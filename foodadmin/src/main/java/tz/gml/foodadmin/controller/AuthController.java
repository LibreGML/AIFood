package tz.gml.foodadmin.controller;

import tz.gml.foodadmin.dto.RegisterRequest;
import tz.gml.foodadmin.dto.LoginRequest;
import tz.gml.foodadmin.dto.AuthResponse;
import tz.gml.foodadmin.dto.ApiResponse;
import tz.gml.foodadmin.dto.UserDTO;
import tz.gml.foodadmin.dto.ChangePasswordRequest;
import tz.gml.foodadmin.service.UserService;
import tz.gml.foodadmin.util.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "*")
public class AuthController {
    
    @Autowired
    private UserService userService;
    
    @PostMapping("/register")
    public ResponseEntity<ApiResponse<?>> register(@RequestBody RegisterRequest registerRequest) {
        try {
            AuthResponse response = userService.register(registerRequest);
            return ResponseEntity.ok(ApiResponse.success("注册成功", response));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(ApiResponse.error(e.getMessage()));
        }
    }
    
    @PostMapping("/login")
    public ResponseEntity<ApiResponse<?>> login(@RequestBody LoginRequest loginRequest) {
        try {
            AuthResponse response = userService.login(loginRequest);
            return ResponseEntity.ok(ApiResponse.success("登录成功", response));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(ApiResponse.error(e.getMessage()));
        }
    }
    
    @PostMapping("/change-password")
    public ResponseEntity<ApiResponse<?>> changePassword(@RequestBody ChangePasswordRequest changePasswordRequest,
                                                        @RequestHeader("Authorization") String token) {
        try {
            String username = JwtUtil.getUsernameFromToken(token.replace("Bearer ", ""));
            userService.changePassword(username, changePasswordRequest.getOldPassword(), changePasswordRequest.getNewPassword());
            return ResponseEntity.ok(ApiResponse.success("密码修改成功", null));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(ApiResponse.error(e.getMessage()));
        }
    }
    
    @GetMapping("/user-info")
    public ResponseEntity<ApiResponse<?>> getUserInfo(@RequestHeader("Authorization") String token) {
        try {
            String username = JwtUtil.getUsernameFromToken(token.replace("Bearer ", ""));
            UserDTO userDTO = userService.getUserInfo(username);
            return ResponseEntity.ok(ApiResponse.success("获取用户信息成功", userDTO));
        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(ApiResponse.error(e.getMessage()));
        }
    }
}