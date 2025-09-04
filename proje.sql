-- =============================================================================
-- PROJE: GELİŞTİRİLMİŞ ÇOK SEKTÖRLÜ HİZMET PLATFORMU VERİTABANI ŞEMASI
-- VERİTABANI: MySQL 8+
--
-- AÇIKLAMA:
-- Bu şema, "soft delete", "audit log", iş/teklif sistemi ve portfolyo
-- gibi modern özelliklerle zenginleştirilmiş, MySQL için optimize edilmiştir.
--
-- TEMEL ÖZELLİKLER:
-- 1. MySQL Uyumluluğu: Tamamen MySQL 8+ sözdizimi ile oluşturulmuştur.
-- 2. Soft Deletes: Kayıtlar 'is_active' alanı ile pasife çekilir.
-- 3. Gelişmiş Audit Trail: Hangi kullanıcının hangi veriyi ne zaman
--    değiştirdiği JSON formatında detaylıca loglanır.
-- 4. İş & Teklif Sistemi: Müşteriler iş talebi oluşturur, sağlayıcılar teklif verir.
-- 5. Puan & Yorum Sistemi: Tamamlanan işler için değerlendirme altyapısı.
-- 6. Portfolyo: Sağlayıcıların çalışmalarını sergilemesi için alan.
-- =============================================================================

-- Veritabanı oluşturma ve seçme
CREATE DATABASE IF NOT EXISTS `platform_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `platform_db`;

-- =============================================================================
-- TEMEL TABLOLAR (Kullanıcılar, Roller, Lokasyonlar, Hizmetler)
-- =============================================================================

CREATE TABLE `roles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `role_name` ENUM('admin', 'provider', 'customer') NOT NULL UNIQUE,
    `description` TEXT
);

INSERT INTO `roles` (`role_name`, `description`) VALUES
('admin', 'Sistem yöneticisi, tam yetkili.'),
('provider', 'Hizmet sağlayan (usta, avukat, vb.).'),
('customer', 'Hizmet arayan son kullanıcı.')
ON DUPLICATE KEY UPDATE `role_name`=`role_name`;

CREATE TABLE `users` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `role_id` INT NOT NULL,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NOT NULL,
    `phone_number` VARCHAR(20) UNIQUE,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`)
);

CREATE TABLE `categories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(150) NOT NULL UNIQUE,
    `slug` VARCHAR(150) NOT NULL UNIQUE,
    `description` TEXT,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE `services` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `category_id` INT NOT NULL,
    `name` VARCHAR(150) NOT NULL,
    `slug` VARCHAR(150) NOT NULL,
    `description` TEXT,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `uk_service_category_name` (`category_id`, `name`),
    FOREIGN KEY (`category_id`) REFERENCES `categories`(`id`)
);

CREATE TABLE `cities` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL UNIQUE,
    `slug` VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE `districts` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `city_id` INT NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `slug` VARCHAR(100) NOT NULL,
    UNIQUE KEY `uk_district_city_name` (`city_id`, `name`),
    FOREIGN KEY (`city_id`) REFERENCES `cities`(`id`)
);

CREATE TABLE `providers` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT NOT NULL UNIQUE,
    `company_name` VARCHAR(255),
    `profile_bio` TEXT,
    `profile_picture_url` VARCHAR(512),
    `is_verified` BOOLEAN NOT NULL DEFAULT FALSE,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
);

CREATE TABLE `provider_service_areas` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `provider_id` BIGINT NOT NULL,
    `service_id` INT NOT NULL,
    `district_id` INT NOT NULL,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `uk_provider_service_district` (`provider_id`, `service_id`, `district_id`),
    FOREIGN KEY (`provider_id`) REFERENCES `providers`(`id`),
    FOREIGN KEY (`service_id`) REFERENCES `services`(`id`),
    FOREIGN KEY (`district_id`) REFERENCES `districts`(`id`)
);


-- =============================================================================
-- YENİ EKLENEN FONKSİYONEL TABLOLAR (İş, Teklif, Yorum, Portfolyo)
-- =============================================================================

CREATE TABLE `jobs` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `customer_id` BIGINT NOT NULL,
    `service_id` INT NOT NULL,
    `district_id` INT NOT NULL,
    `title` VARCHAR(255) NOT NULL,
    `description` TEXT NOT NULL,
    `status` ENUM('open', 'assigned', 'completed', 'cancelled') NOT NULL DEFAULT 'open',
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`customer_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`service_id`) REFERENCES `services`(`id`),
    FOREIGN KEY (`district_id`) REFERENCES `districts`(`id`)
);

CREATE TABLE `offers` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `job_id` BIGINT NOT NULL,
    `provider_id` BIGINT NOT NULL,
    `offer_price` DECIMAL(10, 2) NOT NULL,
    `message` TEXT,
    `status` ENUM('pending', 'accepted', 'rejected', 'withdrawn') NOT NULL DEFAULT 'pending',
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`job_id`) REFERENCES `jobs`(`id`),
    FOREIGN KEY (`provider_id`) REFERENCES `providers`(`id`)
);

CREATE TABLE `reviews` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `job_id` BIGINT NOT NULL UNIQUE, -- Bir işe sadece bir yorum yapılabilir
    `provider_id` BIGINT NOT NULL,
    `customer_id` BIGINT NOT NULL,
    `rating` TINYINT UNSIGNED NOT NULL CHECK (`rating` BETWEEN 1 AND 5),
    `comment` TEXT,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`job_id`) REFERENCES `jobs`(`id`),
    FOREIGN KEY (`provider_id`) REFERENCES `providers`(`id`),
    FOREIGN KEY (`customer_id`) REFERENCES `users`(`id`)
);

CREATE TABLE `portfolio_items` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `provider_id` BIGINT NOT NULL,
    `title` VARCHAR(255) NOT NULL,
    `description` TEXT,
    `image_url` VARCHAR(512) NOT NULL,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`provider_id`) REFERENCES `providers`(`id`)
);


-- =============================================================================
-- DENETİM KAYDI (AUDIT LOG) TABLOSU VE TRIGGER'LARI
-- =============================================================================

CREATE TABLE `audit_logs` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `user_id` BIGINT,
    `action` ENUM('INSERT', 'UPDATE', 'SOFT_DELETE') NOT NULL,
    `table_name` VARCHAR(100) NOT NULL,
    `record_id` VARCHAR(100) NOT NULL,
    `old_values` JSON,
    `new_values` JSON,
    `action_timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Örnek: 'providers' tablosu için denetim trigger'ları
-- DİKKAT: Diğer önemli tablolar (users, services vb.) için de benzer trigger'lar oluşturulmalıdır.
-- Backend tarafında her işlemden önce SET @current_user_id = [yapan_kullanicinin_idsi]; komutu çalıştırılmalıdır.

DELIMITER $$

CREATE TRIGGER `tr_audit_providers_insert`
AFTER INSERT ON `providers`
FOR EACH ROW
BEGIN
    INSERT INTO `audit_logs` (`user_id`, `action`, `table_name`, `record_id`, `new_values`)
    VALUES (
        @current_user_id,
        'INSERT',
        'providers',
        NEW.id,
        JSON_OBJECT(
            'user_id', NEW.user_id,
            'company_name', NEW.company_name,
            'profile_bio', NEW.profile_bio,
            'is_verified', NEW.is_verified,
            'is_active', NEW.is_active
        )
    );
END$$

CREATE TRIGGER `tr_audit_providers_update`
AFTER UPDATE ON `providers`
FOR EACH ROW
BEGIN
    DECLARE v_action ENUM('INSERT', 'UPDATE', 'SOFT_DELETE') DEFAULT 'UPDATE';

    -- Soft delete durumunu yakala
    IF OLD.is_active = TRUE AND NEW.is_active = FALSE THEN
        SET v_action = 'SOFT_DELETE';
    END IF;

    -- Sadece gerçekten bir değişiklik varsa logla
    IF NOT (OLD.company_name <=> NEW.company_name AND
            OLD.profile_bio <=> NEW.profile_bio AND
            OLD.is_verified <=> NEW.is_verified AND
            OLD.is_active <=> NEW.is_active)
    THEN
        INSERT INTO `audit_logs` (`user_id`, `action`, `table_name`, `record_id`, `old_values`, `new_values`)
        VALUES (
            @current_user_id,
            v_action,
            'providers',
            OLD.id,
            JSON_OBJECT(
                'company_name', OLD.company_name,
                'profile_bio', OLD.profile_bio,
                'is_verified', OLD.is_verified,
                'is_active', OLD.is_active
            ),
            JSON_OBJECT(
                'company_name', NEW.company_name,
                'profile_bio', NEW.profile_bio,
                'is_verified', NEW.is_verified,
                'is_active', NEW.is_active
            )
        );
    END IF;
END$$

DELIMITER ;
