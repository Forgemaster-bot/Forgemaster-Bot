USE [master]
GO
/****** Object:  Database [LostWorld]    Script Date: 9/8/2020 1:03:10 PM ******/
CREATE DATABASE [LostWorld]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'LostWorld', FILENAME = N'/var/opt/mssql/data/LostWorld.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'LostWorld_log', FILENAME = N'/var/opt/mssql/data/LostWorld_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [LostWorld] SET COMPATIBILITY_LEVEL = 140
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [LostWorld].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [LostWorld] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [LostWorld] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [LostWorld] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [LostWorld] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [LostWorld] SET ARITHABORT OFF 
GO
ALTER DATABASE [LostWorld] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [LostWorld] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [LostWorld] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [LostWorld] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [LostWorld] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [LostWorld] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [LostWorld] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [LostWorld] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [LostWorld] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [LostWorld] SET  DISABLE_BROKER 
GO
ALTER DATABASE [LostWorld] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [LostWorld] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [LostWorld] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [LostWorld] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [LostWorld] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [LostWorld] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [LostWorld] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [LostWorld] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [LostWorld] SET  MULTI_USER 
GO
ALTER DATABASE [LostWorld] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [LostWorld] SET DB_CHAINING OFF 
GO
ALTER DATABASE [LostWorld] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [LostWorld] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [LostWorld] SET DELAYED_DURABILITY = DISABLED 
GO
EXEC sys.sp_db_vardecimal_storage_format N'LostWorld', N'ON'
GO
ALTER DATABASE [LostWorld] SET QUERY_STORE = OFF
GO
ALTER DATABASE [LostWorld] SET  READ_WRITE 
GO
