// Copyright Epic Games, Inc. All Rights Reserved.

#include "GAPACommands.h"

#define LOCTEXT_NAMESPACE "FGAPAModule"

void FGAPACommands::RegisterCommands()
{
	UI_COMMAND(PluginAction, "GAPA", "Execute GAPA action", EUserInterfaceActionType::Button, FInputChord());
}

#undef LOCTEXT_NAMESPACE
