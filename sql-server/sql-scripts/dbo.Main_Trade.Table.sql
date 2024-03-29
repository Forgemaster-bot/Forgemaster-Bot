USE [LostWorld]
GO
/****** Object:  Table [dbo].[Main_Trade]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Main_Trade](
	[Character_ID] [uniqueidentifier] NOT NULL,
	[Item] [nvarchar](50) NOT NULL,
	[Quantity] [int] NOT NULL,
	[Price] [float] NOT NULL,
	[Type] [nvarchar](50) NOT NULL
) ON [PRIMARY]
GO
