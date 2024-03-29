USE [LostWorld]
GO
/****** Object:  Table [dbo].[Info_Item]    Script Date: 9/8/2020 1:03:10 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Info_Item](
	[Name] [nvarchar](50) NOT NULL,
	[Description] [nvarchar](max) NULL,
	[Weight] [float] NULL,
	[Value] [float] NULL,
	[Type] [nvarchar](50) NULL,
	[Crafting] [nvarchar](50) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Hide Armour Barding', NULL, 24, 40, N'Mounts and Vehicles', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Exotic Saddle', NULL, 40, 60, N'Mounts and Vehicles', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Military Saddle', NULL, 30, 20, N'Mounts and Vehicles', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Pack Saddle', NULL, 15, 5, N'Mounts and Vehicles', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Riding Saddle', NULL, 25, 10, N'Mounts and Vehicles', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Saddlebag', NULL, 8, 4, N'Mounts and Vehicles', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Whip', NULL, 3, 2, N'Melee Weapon', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Sling', NULL, 0.5, 0.1, N'Ranged Weapon', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Ball Bearings', NULL, 2, 1, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Caltrops', NULL, 2, 1, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Chain - 10 feet', NULL, 10, 5, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Crowbar', NULL, 5, 2, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Grappling Hook', NULL, 4, 2, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Hammer', NULL, 3, 1, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Sledge Hammer', NULL, 10, 2, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Holy Symbol - Amulet', NULL, 1, 5, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Holy Symbol - Emblem', NULL, 0, 5, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Manacles', NULL, 6, 2, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Mess Kit', NULL, 1, 0.2, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Steel Mirror', NULL, 0.5, 5, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Hunting Trap', NULL, 25, 5, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Mining Pick', NULL, 10, 2, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Piton', NULL, 0.25, 0.05, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Iron Pot', NULL, 10, 2, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Scale, Merchant', NULL, 3, 5, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Iron Spikes', NULL, 0.5, 0.1, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Shovel', NULL, 5, 2, N'Adventure Gear', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Chain shirt', NULL, 20, 50, N'Armor', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Scale mail', NULL, 45, 50, N'Armor', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Breastplate', NULL, 20, 400, N'Armor', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Half plate', NULL, 40, 750, N'Armor', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Ring mail', NULL, 40, 30, N'Armor', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Chain mail', NULL, 55, 75, N'Armor', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Splint', NULL, 60, 200, N'Armor', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Plate', NULL, 65, 1500, N'Armor', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Dagger', NULL, 1, 2, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Handaxe', NULL, 2, 5, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Light Hammer', NULL, 2, 2, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Mace', NULL, 4, 5, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Sickle', NULL, 2, 1, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Dart', NULL, 0.25, 0.05, N'Ranged Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Battleaxe', NULL, 4, 10, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Flail', NULL, 2, 10, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Glaive', NULL, 6, 20, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Greataxe', NULL, 7, 30, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Greatsword', NULL, 6, 50, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Halberd', NULL, 6, 20, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Lance', NULL, 6, 10, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Longsword', NULL, 3, 15, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Maul', NULL, 10, 10, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Morningstar', NULL, 4, 15, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Rapier', NULL, 2, 25, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Scimitar', NULL, 3, 25, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Shortsword', NULL, 2, 10, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Trident', NULL, 4, 5, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'War Pick', NULL, 2, 5, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Warhammer', NULL, 2, 15, N'Melee Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Carpenters tools', NULL, 6, 8, N'Tools', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Cooks utensils', NULL, 8, 1, N'Tools', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Leatherworker tools', NULL, 5, 5, N'Tools', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Smiths tools', NULL, 8, 20, N'Tools', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Chain shirt Barding', NULL, 40, 200, N'Mounts and Vehicles', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Scale mail Barding', NULL, 90, 200, N'Mounts and Vehicles', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Breastplate Barding', NULL, 40, 1600, N'Mounts and Vehicles', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Half plate Barding', NULL, 80, 3000, N'Mounts and Vehicles', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Ring mail Barding', NULL, 80, 120, N'Mounts and Vehicles', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Chain mail Barding', NULL, 110, 300, N'Mounts and Vehicles', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Splint Barding', NULL, 120, 800, N'Mounts and Vehicles', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Dagger', NULL, 0, 102, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Handaxe', NULL, 0, 105, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Light Hammer', NULL, 0, 102, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Mace5', NULL, 0, 105, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Sickle', NULL, 0, 101, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Battleaxe', NULL, 0, 110, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Flail', NULL, 0, 110, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Glaive', NULL, 0, 120, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Greateaxe', NULL, 0, 130, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Greatsword', NULL, 0, 150, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Halberd', NULL, 0, 120, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Lance', NULL, 0, 110, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Longsword', NULL, 0, 115, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Maul', NULL, 0, 110, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Morningstar', NULL, 0, 115, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Rapier', NULL, 0, 125, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Scimitar', NULL, 0, 125, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Shortsword', NULL, 0, 110, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Trident', NULL, 0, 105, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered War Pick', NULL, 0, 105, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Warhammer', NULL, 0, 115, N'Silvered Weapon', N'Smith')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Palm Pistol', NULL, 1, 50, N'Ranged Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Pistol', NULL, 3, 150, N'Ranged Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Musket', NULL, 10, 300, N'Ranged Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Pepperbox', NULL, 5, 250, N'Ranged Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Blunderbuss', NULL, 10, 300, N'Ranged Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Bad News', NULL, 25, 750, N'Ranged Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Hand Mortar', NULL, 10, 800, N'Ranged Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Palm Pistol Ammo', NULL, 0.1, 0.1, N'Ranged Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Pistol Ammo', NULL, 0.1, 0.2, N'Ranged Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Musket Ammo', NULL, 0.1, 0.25, N'Ranged Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Pepperbox Ammo', NULL, 0.1, 0.2, N'Ranged Weapon', N'Tinker')
GO
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Blunderbuss Ammo', NULL, 0.5, 1, N'Ranged Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Bell', NULL, 0, 1, N'Adventure Gear', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Tinker Tools', NULL, 10, 25, N'Tools', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Bullseye Lantern', NULL, 2, 10, N'Adventure Gear', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Hooded Lantern', NULL, 2, 5, N'Adventure Gear', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Lock', NULL, 1, 10, N'Adventure Gear', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Signet Ring', NULL, 0, 5, N'Adventure Gear', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Whetstone', NULL, 1, 0.01, N'Adventure Gear', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Spyglass', NULL, 1, 1000, N'Adventure Gear', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Magnifying Glass', NULL, 0, 100, N'Adventure Gear', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Hourglass', NULL, 1, 25, N'Adventure Gear', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Thieves tools', NULL, 1, 25, N'Tools', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Blunderbuss Ammo5', NULL, 0, 10.5, N'Silvered Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Musket Ammo', NULL, 0, 10.25, N'Silvered Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Palm Pistol Ammo', NULL, 0, 10.1, N'Silvered Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Pepperbox Ammo', NULL, 0, 10.2, N'Silvered Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Pistol Ammo', NULL, 0, 10.2, N'Silvered Weapon', N'Tinker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Basket', NULL, 2, 0.4, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Bedroll', NULL, 7, 1, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Blanket', NULL, 3, 0.5, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Climber Kit', NULL, 12, 25, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Common Clothes', NULL, 3, 0.5, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Costume Clothes', NULL, 4, 5, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Fine Clothes', NULL, 6, 15, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Travelers Clothes', NULL, 4, 2, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Component Pouch', NULL, 2, 25, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Fishing Tackle', NULL, 4, 1, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Healer kit', NULL, 3, 5, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Paper', NULL, 0, 0.2, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Robes', NULL, 4, 1, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Hempen Rope - 50 feet', NULL, 10, 1, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Sack', NULL, 0.5, 0.01, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Two-person tent', NULL, 20, 2, N'Adventure Gear', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Net', NULL, 3, 1, N'Ranged Weapon', N'Weaver')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Earth', NULL, 0.1, 5, N'Essence', N'')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Fire', NULL, 0.1, 5, N'Essence', N'')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Water', NULL, 0.1, 5, N'Essence', N'')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Air', NULL, 0.1, 5, N'Essence', N'')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Light', NULL, 0.1, 5, N'Essence', N'')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Dark', NULL, 0.1, 5, N'Essence', N'')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Candle', NULL, 0, 0.01, N'Adventure Gear', N'Alchemist')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Flask', NULL, 1, 0.02, N'Adventure Gear', N'Alchemist')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Ink', NULL, 0, 10, N'Adventure Gear', N'Alchemist')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Oil', NULL, 1, 0.1, N'Adventure Gear', N'Alchemist')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Sealing Wax', NULL, 0, 0.4, N'Adventure Gear', N'Alchemist')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Soap', NULL, 0, 0.02, N'Adventure Gear', N'Alchemist')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Vial', NULL, 0, 1, N'Adventure Gear', N'Alchemist')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Alchemist supplies', NULL, 8, 50, N'Tools', N'Alchemist')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Poisoner Kit', NULL, 8, 50, N'Tools', N'Alchemist')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Herbalism Kit', NULL, 8, 5, N'Tools', N'Alchemist')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Glass Bottle', NULL, 2, 2, N'Adventure Gear', N'Alchemist')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Abacus', NULL, 2, 2, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Arcane Focus, Rod', NULL, 2, 10, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Arcane Focus, Staff', NULL, 4, 5, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Arcane Focus, Wand', NULL, 1, 10, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Barrel', NULL, 70, 2, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Block and Tackle', NULL, 5, 1, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Bucket', NULL, 2, 0.05, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Chest', NULL, 25, 5, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Crossbow Bolt Case', NULL, 1, 1, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Druidic Focus - Totem', NULL, 0, 1, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Druidic Focus - Wooden Staff', NULL, 4, 5, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Druidic Focus - Yew Wand', NULL, 1, 10, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Ink Pen', NULL, 0, 0.02, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Ladder 10-foot', NULL, 25, 0.1, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Lamp', NULL, 1, 0.5, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Pole 10-foot', NULL, 7, 0.05, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Portable Ram', NULL, 35, 4, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Signal Whistle', NULL, 0, 0.05, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Tinderbox', NULL, 1, 0.5, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Torch', NULL, 1, 0.01, N'Adventure Gear', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Arrow', NULL, 0.05, 0.05, N'Ranged Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Crossbow bolt', NULL, 0.05, 0.05, N'Ranged Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Carriage', NULL, 600, 100, N'Mounts and Vehicles', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Cart', NULL, 200, 15, N'Mounts and Vehicles', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Chariot', NULL, 100, 250, N'Mounts and Vehicles', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Sled', NULL, 300, 20, N'Mounts and Vehicles', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Wagon', NULL, 300, 35, N'Mounts and Vehicles', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Blowgun', NULL, 1, 10, N'Ranged Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Hand Crossbow', NULL, 3, 75, N'Ranged Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Heavy Crossbow', NULL, 18, 50, N'Ranged Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Longbow', NULL, 2, 50, N'Ranged Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Light Crossbow', NULL, 5, 25, N'Ranged Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Quarterstaff', NULL, 4, 0.2, N'Melee Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Javelin', NULL, 2, 0.5, N'Melee Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Sheild', NULL, 6, 10, N'Armor', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Club', NULL, 2, 0.1, N'Melee Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Greatclub', NULL, 10, 0.2, N'Melee Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Weavers tools', NULL, 5, 1, N'Tools', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Pike', NULL, 18, 5, N'Melee Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Spear', NULL, 3, 1, N'Melee Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Shortbow', NULL, 2, 25, N'Ranged Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Calligrapher Supplies', NULL, 8, 10, N'Tools', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Arrow', NULL, 0, 10.05, N'Silvered Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Spear', NULL, 0, 101, N'Silvered Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Silvered Pike', NULL, 0, 105, N'Silvered Weapon', N'Carpenter')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Rations', NULL, 2, 0.5, N'Adventure Gear', N'Cook')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Animal Feed', NULL, 10, 0.05, N'Mounts and Vehicles', N'Cook')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Backpack', NULL, 5, 2, N'Adventure Gear', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Book', NULL, 5, 25, N'Adventure Gear', N'Leatherworker')
GO
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Map or Scroll Case', NULL, 1, 1, N'Adventure Gear', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Parchment', NULL, 0, 0.1, N'Adventure Gear', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Quiver', NULL, 1, 1, N'Adventure Gear', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Spellbook', NULL, 3, 50, N'Adventure Gear', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Waterskin', NULL, 5, 0.2, N'Adventure Gear', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Padded Armor', NULL, 8, 5, N'Armor', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Leather Armor', NULL, 10, 10, N'Armor', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Studded leather Armor', NULL, 13, 45, N'Armor', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Hide Armor', NULL, 12, 10, N'Armor', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Padded Armour Barding', NULL, 16, 20, N'Mounts and Vehicles', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Leather Armour Barding', NULL, 20, 40, N'Mounts and Vehicles', N'Leatherworker')
INSERT [dbo].[Info_Item] ([Name], [Description], [Weight], [Value], [Type], [Crafting]) VALUES (N'Studded leather Armour Barding', NULL, 26, 180, N'Mounts and Vehicles', N'Leatherworker')
GO
