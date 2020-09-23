USE [LostWorld]
GO
/****** Object:  Table [dbo].[Main_Crafting]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Main_Crafting](
	[Character_ID] [uniqueidentifier] NOT NULL,
	[Crafting_Value] [float] NOT NULL,
	[Labour_Points] [int] NOT NULL
) ON [PRIMARY]
GO
