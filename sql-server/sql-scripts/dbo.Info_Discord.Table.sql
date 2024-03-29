USE [LostWorld]
GO
/****** Object:  Table [dbo].[Info_Discord]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Info_Discord](
	[ID] [nvarchar](50) NOT NULL,
	[Name] [nvarchar](50) NOT NULL,
	[Character_Number] [int] NOT NULL,
	[Patreon] [bit] NOT NULL,
 CONSTRAINT [PK_Info_Discord] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Info_Discord] ADD  CONSTRAINT [C_Info_Discord_Patreon_d]  DEFAULT ((0)) FOR [Patreon]
GO
