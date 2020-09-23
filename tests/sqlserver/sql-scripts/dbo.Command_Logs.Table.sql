USE [LostWorld]
GO
/****** Object:  Table [dbo].[Command_Logs]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Command_Logs](
	[User_ID] [nvarchar](50) NOT NULL,
	[Command] [nvarchar](max) NOT NULL,
	[DateTime] [datetime] NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
