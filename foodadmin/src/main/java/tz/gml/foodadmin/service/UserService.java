package tz.gml.foodadmin.service;

import tz.gml.foodadmin.entity.User;
import tz.gml.foodadmin.repository.UserRepository;
import tz.gml.foodadmin.dto.RegisterRequest;
import tz.gml.foodadmin.dto.LoginRequest;
import tz.gml.foodadmin.dto.AuthResponse;
import tz.gml.foodadmin.dto.UserDTO;
import tz.gml.foodadmin.util.JwtUtil;
import at.favre.lib.crypto.bcrypt.BCrypt;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    public AuthResponse register(RegisterRequest registerRequest) throws RuntimeException {
        if (userRepository.existsByUsername(registerRequest.getUsername())) {
            throw new RuntimeException("用户名已存在");
        }
        
        if (userRepository.existsByEmail(registerRequest.getEmail())) {
            throw new RuntimeException("邮箱已被注册");
        }
        
        String hashedPassword = BCrypt.withDefaults().hashToString(12, registerRequest.getPassword().toCharArray());
        
        User user = new User();
        user.setUsername(registerRequest.getUsername());
        user.setPassword(hashedPassword);
        user.setEmail(registerRequest.getEmail());
        
        User savedUser = userRepository.save(user);
        
        String token = JwtUtil.generateToken(savedUser.getUsername());
        
        return new AuthResponse(token, savedUser.getUsername(), savedUser.getEmail());
    }
    
    public AuthResponse login(LoginRequest loginRequest) throws RuntimeException {
        Optional<User> userOptional = userRepository.findByUsername(loginRequest.getUsername());
        
        if (!userOptional.isPresent()) {
            throw new RuntimeException("用户不存在");
        }
        
        User user = userOptional.get();
        
        BCrypt.Result result = BCrypt.verifyer().verify(loginRequest.getPassword().toCharArray(), user.getPassword());
        
        if (!result.verified) {
            throw new RuntimeException("密码错误");
        }
        
        String token = JwtUtil.generateToken(user.getUsername());
        
        return new AuthResponse(token, user.getUsername(), user.getEmail());
    }
    
    public UserDTO getUserInfo(String username) {
        Optional<User> userOptional = userRepository.findByUsername(username);
        if (!userOptional.isPresent()) {
            throw new RuntimeException("用户不存在");
        }
        
        User user = userOptional.get();
        return new UserDTO(user.getId(), user.getUsername(), user.getEmail(), user.getCreatedAt(), user.getUpdatedAt());
    }
    
    public void changePassword(String username, String oldPassword, String newPassword) {
        Optional<User> userOptional = userRepository.findByUsername(username);
        if (!userOptional.isPresent()) {
            throw new RuntimeException("用户不存在");
        }
        
        User user = userOptional.get();
        
        // 验证旧密码
        BCrypt.Result result = BCrypt.verifyer().verify(oldPassword.toCharArray(), user.getPassword());
        if (!result.verified) {
            throw new RuntimeException("旧密码错误");
        }
        
        // 设置新密码
        String hashedPassword = BCrypt.withDefaults().hashToString(12, newPassword.toCharArray());
        user.setPassword(hashedPassword);
        userRepository.save(user);
    }
}