USE [LostWorld]
GO
/****** Object:  Table [dbo].[Discord_Roll]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Discord_Roll](
	[ID] [uniqueidentifier] NULL,
	[Discord_ID] [nvarchar](50) NULL,
	[Roll_1] [int] NULL,
	[Roll_2] [int] NULL,
	[Roll_3] [int] NULL,
	[Roll_4] [int] NULL,
	[Roll_5] [int] NULL,
	[Roll_6] [int] NULL
) ON [PRIMARY]
GO
