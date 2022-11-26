// Copyright Epic Games, Inc. All Rights Reserved.

#include "GAPA.h"
#include "GAPAStyle.h"
#include "GAPACommands.h"
#include "Misc/MessageDialog.h"
#include "ToolMenus.h"

static const FName GAPATabName("GAPA");

#define LOCTEXT_NAMESPACE "FGAPAModule"

void FGAPAModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
	
	FGAPAStyle::Initialize();
	FGAPAStyle::ReloadTextures();

	FGAPACommands::Register();
	
	PluginCommands = MakeShareable(new FUICommandList);

	PluginCommands->MapAction(
		FGAPACommands::Get().PluginAction,
		FExecuteAction::CreateRaw(this, &FGAPAModule::PluginButtonClicked),
		FCanExecuteAction());

	UToolMenus::RegisterStartupCallback(FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FGAPAModule::RegisterMenus));
}

void FGAPAModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.

	UToolMenus::UnRegisterStartupCallback(this);

	UToolMenus::UnregisterOwner(this);

	FGAPAStyle::Shutdown();

	FGAPACommands::Unregister();
}

void FGAPAModule::PluginButtonClicked()
{
	// Put your "OnButtonClicked" stuff here
	FText DialogText = FText::FromString("PluginButtonDialogText");
	GEngine->Exec(NULL, TEXT("py GAPA_start_import()"));
	//FMessageDialog::Open(EAppMsgType::Ok, DialogText);
}

void FGAPAModule::RegisterMenus()
{
	// Owner will be used for cleanup in call to UToolMenus::UnregisterOwner
	FToolMenuOwnerScoped OwnerScoped(this);

	{
		UToolMenu* Menu = UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Window");
		{
			FToolMenuSection& Section = Menu->FindOrAddSection("WindowLayout");
			Section.AddMenuEntryWithCommandList(FGAPACommands::Get().PluginAction, PluginCommands);
		}
	}

	{
		UToolMenu* ToolbarMenu = UToolMenus::Get()->ExtendMenu("LevelEditor.LevelEditorToolBar.PlayToolBar");
		{
			FToolMenuSection& Section = ToolbarMenu->FindOrAddSection("PluginTools");
			{
				FToolMenuEntry& Entry = Section.AddEntry(FToolMenuEntry::InitToolBarButton(FGAPACommands::Get().PluginAction));
				Entry.SetCommandList(PluginCommands);
			}
		}
	}
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FGAPAModule, GAPA)