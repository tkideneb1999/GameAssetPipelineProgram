// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Framework/Commands/Commands.h"
#include "GAPAStyle.h"

class FGAPACommands : public TCommands<FGAPACommands>
{
public:

	FGAPACommands()
		: TCommands<FGAPACommands>(TEXT("GAPA"), NSLOCTEXT("Contexts", "GAPA", "GAPA Plugin"), NAME_None, FGAPAStyle::GetStyleSetName())
	{
	}

	// TCommands<> interface
	virtual void RegisterCommands() override;

public:
	TSharedPtr< FUICommandInfo > PluginAction;
};
