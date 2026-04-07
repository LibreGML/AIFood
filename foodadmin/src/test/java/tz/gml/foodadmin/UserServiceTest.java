package tz.gml.foodadmin;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import tz.gml.foodadmin.dto.ChangePasswordRequest;
import tz.gml.foodadmin.dto.UserDTO;
import tz.gml.foodadmin.service.UserService;
import tz.gml.foodadmin.dto.RegisterRequest;
import tz.gml.foodadmin.dto.AuthResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@Transactional
public class UserServiceTest {

    @Autowired
    private UserService userService;

    @Test
    public void testChangePassword() {
        // 注册一个测试用户
        RegisterRequest registerRequest = new RegisterRequest("testuser", "oldpassword", "test@example.com");
        AuthResponse response = userService.register(registerRequest);

        // 修改密码
        assertDoesNotThrow(() -> {
            userService.changePassword("testuser", "oldpassword", "newpassword");
        });

        // 尝试用新密码登录
        // 这里需要在实际应用中测试
    }

    @Test
    public void testGetUserInfo() {
        // 注册一个测试用户
        RegisterRequest registerRequest = new RegisterRequest("infouser", "password", "info@example.com");
        AuthResponse response = userService.register(registerRequest);

        // 获取用户信息
        UserDTO userDTO = userService.getUserInfo("infouser");
        
        assertNotNull(userDTO);
        assertEquals("infouser", userDTO.getUsername());
        assertEquals("info@example.com", userDTO.getEmail());
        assertNotNull(userDTO.getCreatedAt());
        assertNotNull(userDTO.getUpdatedAt());
    }
}