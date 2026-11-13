import os
import sys
import json
import urllib.parse
import http.server
import socketserver
import requests

CLIENT_ID = os.environ.get("LINKEDIN_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET", "")
REDIRECT_URI = "http://localhost:8080/callback"
PORT = 8080

SCOPES = ["w_member_social", "openid", "profile"]

def get_auth_url(redirect_uri=REDIRECT_URI):
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": redirect_uri,
        "scope": " ".join(SCOPES),
        "state": "antigravity_secure_state_12345"
    }
    return f"https://www.linkedin.com/oauth/v2/authorization?{urllib.parse.urlencode(params)}"

def exchange_code_for_token(code, redirect_uri=REDIRECT_URI):
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": redirect_uri
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    res = requests.post(url, data=payload, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception(f"Failed to get token: {res.status_code} {res.text}")

def get_user_urn(access_token):
    # LinkedIn OpenID Connect UserInfo endpoint
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        sub = data.get("sub")
        name = data.get("name", "Unknown")
        return f"urn:li:person:{sub}", name
    else:
        # Fallback to legacy me endpoint
        url2 = "https://api.linkedin.com/v2/me"
        res2 = requests.get(url2, headers=headers)
        if res2.status_code == 200:
            data = res2.json()
            return f"urn:li:person:{data.get('id')}", "User"
        raise Exception(f"Failed to get user profile: {res.status_code} {res.text}")

def upload_image_rest(access_token, person_urn, image_path):
    """Initializes image upload and uploads binary to LinkedIn REST API."""
    init_url = "https://api.linkedin.com/rest/images?action=initializeUpload"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202401",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    init_payload = {
        "initializeUploadRequest": {
            "owner": person_urn
        }
    }
    init_res = requests.post(init_url, json=init_payload, headers=headers)
    if init_res.status_code != 200:
        # Try v2 UGC upload fallback
        return upload_image_v2(access_token, person_urn, image_path)

    init_data = init_res.json().get("value", {})
    upload_url = init_data.get("uploadUrl")
    image_urn = init_data.get("image")

    with open(image_path, "rb") as img_file:
        up_res = requests.put(upload_url, data=img_file, headers={"Content-Type": "image/png"})
        if up_res.status_code not in (200, 201):
            raise Exception(f"Failed to upload image binary: {up_res.status_code}")

    return image_urn

def upload_image_v2(access_token, person_urn, image_path):
    """Fallback using LinkedIn v2 Assets API"""
    url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": person_urn,
            "serviceRelationships": [{
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }]
        }
    }
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code != 200:
        raise Exception(f"Assets register failed: {res.status_code} {res.text}")
    val = res.json().get("value", {})
    asset = val.get("asset")
    upload_url = val.get("uploadMechanism", {}).get("com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest", {}).get("uploadUrl")

    with open(image_path, "rb") as f:
        put_res = requests.put(upload_url, data=f, headers={"Content-Type": "image/png"})
        if put_res.status_code not in (200, 201):
            raise Exception(f"Binary upload failed: {put_res.status_code}")
    return asset

def create_post(access_token, person_urn, commentary_text, image_urns=None):
    """Publishes post via Posts REST API or UGC API"""
    # 1. Try Posts REST API
    post_url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "LinkedIn-Version": "202401",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    content_dict = {}
    if image_urns:
        if len(image_urns) == 1:
            content_dict = {
                "media": {
                    "id": image_urns[0]
                }
            }
        else:
            content_dict = {
                "multiImage": {
                    "images": [{"id": urn} for urn in image_urns]
                }
            }

    payload = {
        "author": person_urn,
        "commentary": commentary_text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }
    if content_dict:
        payload["content"] = content_dict

    res = requests.post(post_url, json=payload, headers=headers)
    if res.status_code in (201, 200):
        return res.headers.get("x-restli-id", "Success")

    # Fallback to UGC post API
    ugc_url = "https://api.linkedin.com/v2/ugcPosts"
    ugc_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    media_list = []
    if image_urns:
        for urn in image_urns:
            media_list.append({
                "status": "READY",
                "media": urn,
                "title": {"text": "Benchmark Terminal Comparison"}
            })

    ugc_payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": commentary_text},
                "shareMediaCategory": "IMAGE" if image_urns else "NONE",
                "media": media_list if image_urns else []
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    res2 = requests.post(ugc_url, json=ugc_payload, headers=ugc_headers)
    if res2.status_code in (200, 201):
        return res2.json().get("id", "Success")
    raise Exception(f"Failed to post: {res.status_code} ({res.text}) | Fallback: {res2.status_code} ({res2.text})")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "auth-url":
        redirect = sys.argv[2] if len(sys.argv) > 2 else REDIRECT_URI
        print(get_auth_url(redirect))

