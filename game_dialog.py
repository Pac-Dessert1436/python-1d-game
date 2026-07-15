import pygame
from dataclasses import dataclass
from typing import Optional, Callable


class GameDialog:
    @dataclass
    class __Result:
        ok: bool = False
        value: str = ""

    def __init__(self, screen: pygame.Surface, font_path: str):
        self.screen = screen
        self.font_name = font_path
        self.title_font = pygame.font.Font(font_path, 28)
        self.content_font = pygame.font.Font(font_path, 24)
        self.input_font = pygame.font.Font(font_path, 24)
        self.button_font = pygame.font.Font(font_path, 22)

        self.bg_color = (50, 50, 60)
        self.border_color = (100, 100, 120)
        self.text_color = (255, 255, 255)
        self.input_bg_color = (30, 30, 40)
        self.button_color = (70, 130, 180)
        self.button_hover_color = (100, 149, 237)
        self.button_text_color = (255, 255, 255)
        
    def msg_box(self, message: str, title: str, buttons: Optional[list[str]] = None) -> GameDialog.__Result:
        if buttons is None:
            buttons = ["OK"]
        
        # 处理多行消息
        lines = message.split('\n')
        
        # 计算对话框尺寸
        padding = 20
        title_height = 50
        line_height = 28
        button_height = 40
        button_width = 100
        button_spacing = 20
        
        content_height = len(lines) * line_height
        content_width = max(self.content_font.size(line)[0] for line in lines)
        title_width = self.title_font.size(title)[0]
        
        dialog_width = max(content_width, title_width) + padding * 2
        dialog_height = title_height + content_height + button_height + padding * 3
        
        # 确保按钮区域足够
        buttons_width = len(buttons) * button_width + (len(buttons) - 1) * button_spacing
        if buttons_width > dialog_width:
            dialog_width = buttons_width + padding * 2
        
        dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
        screen_rect = self.screen.get_rect()
        dialog_rect = dialog_surface.get_rect(center=screen_rect.center)
        
        button_rects = []
        total_buttons_width = len(buttons) * button_width + (len(buttons) - 1) * button_spacing
        start_x = (dialog_width - total_buttons_width) // 2
        button_y = dialog_height - button_height - padding
        
        for i, button_text in enumerate(buttons):
            button_x = start_x + i * (button_width + button_spacing)
            button_rects.append(pygame.Rect(button_x, button_y, button_width, button_height))
        
        running = True
        hover_index = -1
        result = GameDialog.__Result(ok=False)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameDialog.__Result(ok=False, value="QUIT")
                
                if event.type == pygame.MOUSEMOTION:
                    hover_index = -1
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(event.pos):
                            local_pos = (event.pos[0] - dialog_rect.x, event.pos[1] - dialog_rect.y)
                            if rect.collidepoint(local_pos):
                                hover_index = i
                                break
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i, rect in enumerate(button_rects):
                            local_pos = (event.pos[0] - dialog_rect.x, event.pos[1] - dialog_rect.y)
                            if rect.collidepoint(local_pos):
                                result.ok = True
                                result.value = buttons[i]
                                running = False
                                break
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return GameDialog.__Result(ok=False, value="CANCEL")
                    elif event.key == pygame.K_RETURN and len(buttons) > 0:
                        result.ok = True
                        result.value = buttons[0]
                        running = False
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        idx = event.key - pygame.K_1
                        if idx < len(buttons):
                            result.ok = True
                            result.value = buttons[idx]
                            running = False
            
            dialog_surface.fill(self.bg_color)
            pygame.draw.rect(dialog_surface, self.border_color, dialog_surface.get_rect(), 2)
            title_text = self.title_font.render(title, True, self.text_color)
            title_rect = title_text.get_rect(center=(dialog_width // 2, title_height // 2))
            dialog_surface.blit(title_text, title_rect)
            
            for i, line in enumerate(lines):
                text = self.content_font.render(line, True, self.text_color)
                text_y = title_height + padding + i * line_height
                text_rect = text.get_rect(center=(dialog_width // 2, text_y))
                dialog_surface.blit(text, text_rect)
            
            for i, (button_text, rect) in enumerate(zip(buttons, button_rects)):
                color = self.button_hover_color if i == hover_index else self.button_color
                pygame.draw.rect(dialog_surface, color, rect, border_radius=5)
                pygame.draw.rect(dialog_surface, self.border_color, rect, 2, border_radius=5)
                display_text = f"{i + 1}. {button_text}" if len(buttons) > 1 else button_text
                button_label = self.button_font.render(display_text, True, self.button_text_color)
                label_rect = button_label.get_rect(center=rect.center)
                dialog_surface.blit(button_label, label_rect)
            
            self.screen.blit(dialog_surface, dialog_rect)
            pygame.display.flip()
        
        return result
    
    def input_box(self, prompt: str, title: str = "Input", default: str = "", 
                  validator: Optional[Callable[[str], bool]] = None) -> GameDialog.__Result:
        lines = prompt.split('\n')

        padding = 20
        title_height = 50
        line_height = 28
        input_height = 40
        button_height = 40
        button_width = 100
        
        content_height = len(lines) * line_height
        content_width = max(self.content_font.size(line)[0] for line in lines)
        title_width = self.title_font.size(title)[0]
        
        dialog_width = max(content_width, title_width, 300) + padding * 2
        dialog_height = title_height + content_height + input_height + button_height + padding * 4
        
        # 创建对话框Surface
        dialog_surface = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
        
        # 居中显示
        screen_rect = self.screen.get_rect()
        dialog_rect = dialog_surface.get_rect(center=screen_rect.center)
        
        # 输入框区域
        input_rect = pygame.Rect(padding, title_height + content_height + padding * 2, 
                                 dialog_width - padding * 2, input_height)
        
        # 按钮区域
        button_width = 100
        cancel_button_rect = pygame.Rect(padding, dialog_height - button_height - padding, 
                                         button_width, button_height)
        ok_button_rect = pygame.Rect(dialog_width - button_width - padding, 
                                     dialog_height - button_height - padding, 
                                     button_width, button_height)
        
        clock = pygame.time.Clock()
        running = True
        hover_ok = False
        hover_cancel = False
        input_text = default
        input_active = True
        blink_timer = 0
        show_cursor = True
        result = GameDialog.__Result(ok=False, value=default)
        
        while running:
            dt = clock.tick(60)
            blink_timer += dt
            if blink_timer > 500:
                blink_timer = 0
                show_cursor = not show_cursor
            
            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameDialog.__Result(ok=False, value="QUIT")
                
                if event.type == pygame.MOUSEMOTION:
                    local_pos = (event.pos[0] - dialog_rect.x, event.pos[1] - dialog_rect.y)
                    hover_ok = ok_button_rect.collidepoint(local_pos)
                    hover_cancel = cancel_button_rect.collidepoint(local_pos)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        local_pos = (event.pos[0] - dialog_rect.x, event.pos[1] - dialog_rect.y)
                        
                        if ok_button_rect.collidepoint(local_pos):
                            if validator is None or validator(input_text):
                                result.ok = True
                                result.value = input_text
                                running = False
                        elif cancel_button_rect.collidepoint(local_pos):
                            return GameDialog.__Result(ok=False, value=default)
                        elif input_rect.collidepoint(local_pos):
                            input_active = True
                        else:
                            input_active = False
                
                if event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            if validator is None or validator(input_text):
                                result.ok = True
                                result.value = input_text
                                running = False
                        elif event.key == pygame.K_ESCAPE:
                            return GameDialog.__Result(ok=False, value=default)
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                            show_cursor = True
                            blink_timer = 0
                        else:
                            if event.unicode and len(event.unicode) == 1:
                                input_text += event.unicode
                                show_cursor = True
                                blink_timer = 0
            
            dialog_surface.fill(self.bg_color)
            pygame.draw.rect(dialog_surface, self.border_color, dialog_surface.get_rect(), 2)
            
            title_text = self.title_font.render(title, True, self.text_color)
            title_rect = title_text.get_rect(center=(dialog_width // 2, title_height // 2))
            dialog_surface.blit(title_text, title_rect)
            for i, line in enumerate(lines):
                text = self.content_font.render(line, True, self.text_color)
                text_y = title_height + padding + i * line_height
                text_rect = text.get_rect(center=(dialog_width // 2, text_y))
                dialog_surface.blit(text, text_rect)

            input_color = self.button_hover_color if input_active else self.input_bg_color
            pygame.draw.rect(dialog_surface, input_color, input_rect, border_radius=5)
            pygame.draw.rect(dialog_surface, self.border_color if input_active else self.button_color, 
                            input_rect, 2, border_radius=5)
            
            # 绘制输入文本
            text_surface = self.input_font.render(input_text, True, self.text_color)
            text_x = input_rect.x + 10
            text_y = input_rect.y + (input_height - text_surface.get_height()) // 2
            dialog_surface.blit(text_surface, (text_x, text_y))
            
            if input_active and show_cursor:
                cursor_x = text_x + text_surface.get_width() + 2
                cursor_y = input_rect.y + 8
                cursor_height = input_height - 16
                pygame.draw.line(dialog_surface, self.text_color, 
                               (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

            ok_color = self.button_hover_color if hover_ok else self.button_color
            pygame.draw.rect(dialog_surface, ok_color, ok_button_rect, border_radius=5)
            pygame.draw.rect(dialog_surface, self.border_color, ok_button_rect, 2, border_radius=5)
            ok_text = self.button_font.render("OK", True, self.button_text_color)
            ok_text_rect = ok_text.get_rect(center=ok_button_rect.center)
            dialog_surface.blit(ok_text, ok_text_rect)
            
            cancel_color = self.button_hover_color if hover_cancel else self.button_color
            pygame.draw.rect(dialog_surface, cancel_color, cancel_button_rect, border_radius=5)
            pygame.draw.rect(dialog_surface, self.border_color, cancel_button_rect, 2, border_radius=5)
            cancel_text = self.button_font.render("Cancel", True, self.button_text_color)
            cancel_text_rect = cancel_text.get_rect(center=cancel_button_rect.center)
            dialog_surface.blit(cancel_text, cancel_text_rect)

            self.screen.blit(dialog_surface, dialog_rect)
            pygame.display.flip()
        
        return result