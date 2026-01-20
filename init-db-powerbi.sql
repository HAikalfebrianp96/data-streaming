/* =========================================================
   DATABASE & TABLE
   ========================================================= */

USE master;
GO

IF DB_ID('moviesdb') IS NULL
    CREATE DATABASE moviesdb;
GO

USE moviesdb;
GO

IF OBJECT_ID('moviesproject', 'U') IS NOT NULL
    DROP TABLE moviesproject;
GO

CREATE TABLE moviesproject (
    id INT IDENTITY(1,1) PRIMARY KEY,
    show_id VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    title NVARCHAR(MAX),
    director NVARCHAR(MAX),
    cast NVARCHAR(MAX),
    country VARCHAR(200),
    release_year VARCHAR(20),
    rating VARCHAR(20),
    duration VARCHAR(50),
    duration_value INT,
    duration_type VARCHAR(20),
    description NVARCHAR(MAX),
    platform VARCHAR(50),
    category VARCHAR(200),
    created_at DATETIME DEFAULT GETDATE()
);
GO

/* =========================================================
   UNIQUE KEY (WAJIB UNTUK UPSERT)
   ========================================================= */
ALTER TABLE moviesproject
ADD CONSTRAINT uq_moviesproject_show_id UNIQUE (show_id);
GO

/* =========================================================
   STORED PROCEDURE UPSERT
   ========================================================= */
CREATE OR ALTER PROCEDURE upsert_moviesproject
    @show_id VARCHAR(100),
    @type VARCHAR(50),
    @title NVARCHAR(MAX),
    @director NVARCHAR(MAX),
    @cast NVARCHAR(MAX),
    @country VARCHAR(200),
    @release_year VARCHAR(20),
    @rating VARCHAR(20),
    @duration VARCHAR(50),
    @duration_value INT,
    @duration_type VARCHAR(20),
    @description NVARCHAR(MAX),
    @platform VARCHAR(50),
    @category VARCHAR(200)
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (SELECT 1 FROM moviesproject WHERE show_id = @show_id)
    BEGIN
        UPDATE moviesproject
        SET
            type           = @type,
            title          = @title,
            director       = @director,
            cast           = @cast,
            country        = @country,
            release_year   = @release_year,
            rating         = @rating,
            duration       = @duration,
            duration_value = @duration_value,
            duration_type  = @duration_type,
            description    = @description,
            platform       = @platform,
            category       = @category
        WHERE show_id = @show_id;
    END
    ELSE
    BEGIN
        INSERT INTO moviesproject (
            show_id, type, title, director, cast, country,
            release_year, rating, duration,
            duration_value, duration_type,
            description, platform, category
        )
        VALUES (
            @show_id, @type, @title, @director, @cast, @country,
            @release_year, @rating, @duration,
            @duration_value, @duration_type,
            @description, @platform, @category
        );
    END
END;
GO
