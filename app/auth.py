import jwt
from datetime import datetime, timedelta
from flask import request, jsonify

SECRET_KEY = "TEST_KEY"  

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def token_required(func):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            token = token.split(" ")[1]  
            user_id = decode_token(token)
            if not user_id:
                return jsonify({"error": "Invalid or expired token"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  
    return wrapper