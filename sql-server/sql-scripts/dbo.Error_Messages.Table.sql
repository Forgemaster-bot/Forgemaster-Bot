USE [LostWorld]
GO
/****** Object:  Table [dbo].[Error_Messages]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Error_Messages](
	[Discord_ID] [nvarchar](50) NOT NULL,
	[Discord_Command] [nvarchar](50) NOT NULL,
	[Error] [nvarchar](max) NOT NULL,
	[DateTime] [datetime] NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
