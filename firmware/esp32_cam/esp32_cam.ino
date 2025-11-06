#include <stdio.h>
#include "esp_camera.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_http_server.h"

#define WIFI_SSID "Arya Robo"
#define WIFI_PASS "Advance@#$"

static const char *TAG = "ESP32-CAM";

// Camera Pin Mapping (AI-Thinker Module)
#define PWDN_GPIO_NUM     -1
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// WiFi Connection Function
void wifi_init() {
    ESP_LOGI(TAG, "Initializing WiFi...");
    esp_netif_init();
    esp_event_loop_create_default();
    esp_netif_create_default_wifi_sta();
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);
    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS
        },
    };
    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_set_config(ESP_IF_WIFI_STA, &wifi_config);
    esp_wifi_start();
    esp_wifi_connect();
}

// HTTP Image Stream Handler
esp_err_t jpg_stream_httpd_handler(httpd_req_t *req) {
    camera_fb_t *fb = NULL;
    char buf[64];
    size_t buf_len;
    esp_err_t res = ESP_OK;

    httpd_resp_set_type(req, "multipart/x-mixed-replace; boundary=frame");

    while (true) {
        fb = esp_camera_fb_get();
        if (!fb) {
            ESP_LOGE(TAG, "Camera capture failed");
            res = ESP_FAIL;
            break;
        }
        buf_len = snprintf(buf, sizeof(buf), 
            "--frame\r\nContent-Type: image/jpeg\r\nContent-Length: %zu\r\n\r\n", fb->len);
        
        res = httpd_resp_send_chunk(req, buf, buf_len);
        res = httpd_resp_send_chunk(req, (const char *)fb->buf, fb->len);
        res = httpd_resp_send_chunk(req, "\r\n", 2);

        esp_camera_fb_return(fb);
        if (res != ESP_OK) {
            break;
        }
    }
    return res;
}

// Start Web Server
void start_webserver() {
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    httpd_handle_t server = NULL;
    if (httpd_start(&server, &config) == ESP_OK) {
        httpd_uri_t uri = {
            .uri = "/stream",
            .method = HTTP_GET,
            .handler = jpg_stream_httpd_handler,
            .user_ctx = NULL
        };
        httpd_register_uri_handler(server, &uri);
    }
}

// Camera Initialization
void camera_init() {
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sscb_sda = SIOD_GPIO_NUM;
    config.pin_sscb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size = FRAMESIZE_QVGA;
    config.jpeg_quality = 12;
    config.fb_count = 2;

    if (esp_camera_init(&config) != ESP_OK) {
        ESP_LOGE(TAG, "Camera initialization failed");
        return;
    }
}

// Main App
void app_main() {
    nvs_flash_init();
    wifi_init();
    camera_init();
    start_webserver();
    ESP_LOGI(TAG, "Stream started! Visit http://<ESP32-IP>/stream");
}
