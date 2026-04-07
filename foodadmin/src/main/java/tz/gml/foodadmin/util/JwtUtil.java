package tz.gml.foodadmin.util;

import cn.hutool.jwt.JWTUtil;
import cn.hutool.jwt.JWT;
import cn.hutool.jwt.signers.JWTSigner;
import cn.hutool.jwt.signers.JWTSignerUtil;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class JwtUtil {
    // 设置30天过期时间
    private static final long EXPIRATION = 1000 * 60 * 60 * 24 * 30L;
    private static final String SECRET = "foodadmin-secret-key-2025";
    
    public static String generateToken(String username) {
        Map<String, Object> map = new HashMap<String, Object>() {{
            put("username", username);
            put("loginTime", System.currentTimeMillis());
        }};
        
        return JWTUtil.createToken(map, SECRET.getBytes());
    }
    
    public static boolean validateToken(String token) {
        try {
            return JWTUtil.verify(token, SECRET.getBytes());
        } catch (Exception e) {
            return false;
        }
    }
    
    public static String getUsernameFromToken(String token) {
        try {
            JWT jwt = JWTUtil.parseToken(token);
            return (String) jwt.getPayload("username");
        } catch (Exception e) {
            return null;
        }
    }
}