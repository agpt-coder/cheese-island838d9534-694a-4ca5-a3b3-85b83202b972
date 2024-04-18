import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

import prisma
import prisma.enums
import project.addItem_service
import project.craftItem_service
import project.createCharacter_service
import project.createDialogue_service
import project.createPuzzle_service
import project.createQuest_service
import project.createSession_service
import project.deleteCharacter_service
import project.deleteDialogue_service
import project.deletePuzzle_service
import project.deleteQuest_service
import project.deleteSession_service
import project.getAllPuzzles_service
import project.getCharacter_service
import project.getCraftingRecipes_service
import project.getDialogue_service
import project.getDialogues_service
import project.getInventoryItems_service
import project.getPuzzle_service
import project.getQuestDetails_service
import project.getQuests_service
import project.getSession_service
import project.listCharacters_service
import project.listSessions_service
import project.markPuzzleCompleted_service
import project.removeItem_service
import project.triggerDialogueEvent_service
import project.updateCharacter_service
import project.updateDialogue_service
import project.updateGameState_service
import project.updateInventoryItem_service
import project.updatePuzzle_service
import project.updateQuest_service
import project.updateSession_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Cheese Island",
    lifespan=lifespan,
    description="A Cheese inspired game based on monkey island",
)


@app.put(
    "/inventory/items/{itemId}",
    response_model=project.updateInventoryItem_service.ItemUpdateResponse,
)
async def api_put_updateInventoryItem(
    itemId: str, quantity: int, status: prisma.enums.ParticipationStatus
) -> project.updateInventoryItem_service.ItemUpdateResponse | Response:
    """
    Updates the details of a specific item in the inventory, like changing its quantity or status. Essential for dynamic gameplay where item attributes might change due to game events.
    """
    try:
        res = project.updateInventoryItem_service.updateInventoryItem(
            itemId, quantity, status
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/puzzles", response_model=project.createPuzzle_service.CreatePuzzleResponse)
async def api_post_createPuzzle(
    title: str, description: str, complexityLevel: int, solution: str
) -> project.createPuzzle_service.CreatePuzzleResponse | Response:
    """
    Creates a new puzzle. This route will allow content creators to define new puzzles that players can solve during gameplay. The API will accept puzzle data such as title, description, complexity level, and solution. The response will include a success status and the created puzzle's ID.
    """
    try:
        res = project.createPuzzle_service.createPuzzle(
            title, description, complexityLevel, solution
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/inventory/items/{itemId}",
    response_model=project.removeItem_service.DeleteInventoryItemResponse,
)
async def api_delete_removeItem(
    itemId: str,
) -> project.removeItem_service.DeleteInventoryItemResponse | Response:
    """
    Removes an item from the inventory by item ID. This endpoint will validate that the item exists and adjust the inventory accordingly. Also, updates interactions with the Character Module for ownership status.
    """
    try:
        res = project.removeItem_service.removeItem(itemId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/inventory/items",
    response_model=project.addItem_service.AddItemToInventoryResponse,
)
async def api_post_addItem(
    characterId: str,
    itemType: prisma.enums.ItemType,
    itemName: str,
    quantity: int,
    description: str,
) -> project.addItem_service.AddItemToInventoryResponse | Response:
    """
    Adds a new item to the inventory. The item details such as type and quantity must be specified. This endpoint will interact with the Character Module to update ownership details.
    """
    try:
        res = project.addItem_service.addItem(
            characterId, itemType, itemName, quantity, description
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/dialogues/{dialogueId}",
    response_model=project.updateDialogue_service.UpdateDialogueResponse,
)
async def api_put_updateDialogue(
    dialogueId: str, newContent: str, linkedCharacterId: Optional[str]
) -> project.updateDialogue_service.UpdateDialogueResponse | Response:
    """
    Updates an existing dialogue script. This endpoint also invokes the Character Module to ensure that updates are consistent with character development.
    """
    try:
        res = project.updateDialogue_service.updateDialogue(
            dialogueId, newContent, linkedCharacterId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/puzzles/{puzzleId}",
    response_model=project.getPuzzle_service.PuzzleDetailsResponse,
)
async def api_get_getPuzzle(
    puzzleId: str, userRole: prisma.enums.UserRole, userId: str
) -> project.getPuzzle_service.PuzzleDetailsResponse | Response:
    """
    Fetches details of a specific puzzle. This route is vital for gameplay, allowing players to receive the necessary puzzle details when they encounter it in the game. It will provide complete details of the puzzle including hints, if they have permissions.
    """
    try:
        res = project.getPuzzle_service.getPuzzle(puzzleId, userRole, userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/multiplayer/session/{sessionId}",
    response_model=project.getSession_service.MultiplayerSessionResponse,
)
async def api_get_getSession(
    sessionId: str,
) -> project.getSession_service.MultiplayerSessionResponse | Response:
    """
    Retrieves details of a specific multiplayer session using the session ID. Details include players' state and current game dynamics.
    """
    try:
        res = project.getSession_service.getSession(sessionId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/dialogues/{dialogueId}",
    response_model=project.deleteDialogue_service.DeleteDialogueResponse,
)
async def api_delete_deleteDialogue(
    dialogueId: str,
) -> project.deleteDialogue_service.DeleteDialogueResponse | Response:
    """
    Removes a dialogue from the system. This will also notify the Puzzle and Quest Modules to ensure that any linked events are also updated or removed accordingly.
    """
    try:
        res = project.deleteDialogue_service.deleteDialogue(dialogueId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/dialogues", response_model=project.getDialogues_service.DialoguesFetchResponse
)
async def api_get_getDialogues(
    request: project.getDialogues_service.DialoguesFetchRequest,
) -> project.getDialogues_service.DialoguesFetchResponse | Response:
    """
    Retrieves a list of current dialogues in the game. Useful for content creators to see what's already in play.
    """
    try:
        res = project.getDialogues_service.getDialogues(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/characters",
    response_model=project.createCharacter_service.CreateCharacterResponse,
)
async def api_post_createCharacter(
    name: str, customizationData: Dict, PlayerProfileId: str
) -> project.createCharacter_service.CreateCharacterResponse | Response:
    """
    Creates a new character with initial attributes and settings based on input parameters. Returns the created character data including ID useful for other operations.
    """
    try:
        res = project.createCharacter_service.createCharacter(
            name, customizationData, PlayerProfileId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/multiplayer/sessions",
    response_model=project.listSessions_service.MultiplayerSessionsResponse,
)
async def api_get_listSessions(
    request: project.listSessions_service.GetMultiplayerSessionsRequest,
) -> project.listSessions_service.MultiplayerSessionsResponse | Response:
    """
    Lists all active multiplayer sessions. Useful for backend monitoring and for players searching for open sessions.
    """
    try:
        res = project.listSessions_service.listSessions(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/inventory/items",
    response_model=project.getInventoryItems_service.InventoryItemsResponse,
)
async def api_get_getInventoryItems(
    request: project.getInventoryItems_service.GetInventoryItemsRequest,
) -> project.getInventoryItems_service.InventoryItemsResponse | Response:
    """
    Retrieves a list of all inventory items available in the player's inventory. This route will fetch the items together with their quantity and status, providing essential information for gameplay.
    """
    try:
        res = project.getInventoryItems_service.getInventoryItems(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/characters/{characterId}",
    response_model=project.getCharacter_service.CharacterFetchResponse,
)
async def api_get_getCharacter(
    characterId: str,
) -> project.getCharacter_service.CharacterFetchResponse | Response:
    """
    Fetches detailed information of a specific character by their ID. Useful for character management and in-game display.
    """
    try:
        res = project.getCharacter_service.getCharacter(characterId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/quests", response_model=project.getQuests_service.QuestsFetchResponse)
async def api_get_getQuests(
    request: project.getQuests_service.QuestsFetchRequest,
) -> project.getQuests_service.QuestsFetchResponse | Response:
    """
    Retrieves a list of all available quests. This route provides a general overview of the quests, mainly metadata such as name, ID, and status. It's useful for both players to see their available quests and admins to monitor quest distribution.
    """
    try:
        res = project.getQuests_service.getQuests(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/inventory/recipes",
    response_model=project.getCraftingRecipes_service.FetchRecipesResponse,
)
async def api_get_getCraftingRecipes(
    request: project.getCraftingRecipes_service.FetchRecipesRequest,
) -> project.getCraftingRecipes_service.FetchRecipesResponse | Response:
    """
    Fetches all possible crafting recipes available to the player, showing required items and quantities. This supports gameplay strategy and planning for item crafting.
    """
    try:
        res = project.getCraftingRecipes_service.getCraftingRecipes(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/quests/{questId}",
    response_model=project.getQuestDetails_service.QuestDetailsResponse,
)
async def api_get_getQuestDetails(
    questId: str,
) -> project.getQuestDetails_service.QuestDetailsResponse | Response:
    """
    Fetches detailed information about a specific quest. This includes all data on quest objectives, rewards, and current progress. Integrates with the Inventory Module for displaying required quest items. Necessary for gameplay progression.
    """
    try:
        res = project.getQuestDetails_service.getQuestDetails(questId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/puzzles", response_model=project.getAllPuzzles_service.GetPuzzlesResponse)
async def api_get_getAllPuzzles(
    request: project.getAllPuzzles_service.GetPuzzlesRequest,
) -> project.getAllPuzzles_service.GetPuzzlesResponse | Response:
    """
    Retrieves a list of all puzzles. This endpoint will be used by admins to monitor and manage puzzles. It could also be used by content creators to get an overview of all available puzzles to adjust or update them accordingly. The response will list details of each puzzle along with metadata like creation dates and usage statistics.
    """
    try:
        res = project.getAllPuzzles_service.getAllPuzzles(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/multiplayer/updateGame",
    response_model=project.updateGameState_service.GameStateUpdateResponse,
)
async def api_post_updateGameState(
    sessionId: str,
    characterChanges: List[project.updateGameState_service.CharacterUpdate],
    inventoryUpdates: List[project.updateGameState_service.InventoryUpdate],
    questUpdates: List[project.updateGameState_service.QuestUpdate],
) -> project.updateGameState_service.GameStateUpdateResponse | Response:
    """
    Broadcasts a game state update to all clients in a session. This might include synchronization of character states, inventory changes, or quest updates.
    """
    try:
        res = project.updateGameState_service.updateGameState(
            sessionId, characterChanges, inventoryUpdates, questUpdates
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/quests/{questId}", response_model=project.deleteQuest_service.DeleteQuestResponse
)
async def api_delete_deleteQuest(
    questId: str,
) -> project.deleteQuest_service.DeleteQuestResponse | Response:
    """
    Permanently removes a quest from the game. It handles the removal of related data in other integrated systems like the Inventory and Narrative Modules. Restricted to Admins to maintain integrity and balance in the game setting.
    """
    try:
        res = project.deleteQuest_service.deleteQuest(questId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/characters", response_model=project.listCharacters_service.GetCharactersResponse
)
async def api_get_listCharacters(
    name: Optional[str],
    createdAfter: Optional[datetime],
    updatedBefore: Optional[datetime],
    userId: Optional[str],
    page: int,
    limit: int,
) -> project.listCharacters_service.GetCharactersResponse | Response:
    """
    Retrieves a list of all created characters. Can be filtered by various parameters for admin and content creator roles.
    """
    try:
        res = project.listCharacters_service.listCharacters(
            name, createdAfter, updatedBefore, userId, page, limit
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/dialogues", response_model=project.createDialogue_service.CreateDialogueResponse
)
async def api_post_createDialogue(
    characterId: str, content: str
) -> project.createDialogue_service.CreateDialogueResponse | Response:
    """
    Allows content creators to add new dialogue scripts into the game. It's expected that this interacts with the Character Module to align new dialogues with character attributes.
    """
    try:
        res = project.createDialogue_service.createDialogue(characterId, content)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/characters/{characterId}",
    response_model=project.deleteCharacter_service.DeleteCharacterResponse,
)
async def api_delete_deleteCharacter(
    characterId: str, admin_user_id: str
) -> project.deleteCharacter_service.DeleteCharacterResponse | Response:
    """
    Removes a character from the system. This action is restricted and typically only available to admins for maintenance or upon specific user requests.
    """
    try:
        res = project.deleteCharacter_service.deleteCharacter(
            characterId, admin_user_id
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/multiplayer/session",
    response_model=project.createSession_service.CreateMultiplayerSessionResponse,
)
async def api_post_createSession(
    hostCharacterId: str,
    participantCharacterIds: List[str],
    sessionType: str,
    initialSettings: Dict[str, Any],
) -> project.createSession_service.CreateMultiplayerSessionResponse | Response:
    """
    Creates a new multiplayer game session. Initializes synchronization with the Character Module. Expected response includes session details such as session ID.
    """
    try:
        res = project.createSession_service.createSession(
            hostCharacterId, participantCharacterIds, sessionType, initialSettings
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/dialogues/{dialogueId}",
    response_model=project.getDialogue_service.DialogueDataResponse,
)
async def api_get_getDialogue(
    dialogueId: str,
) -> project.getDialogue_service.DialogueDataResponse | Response:
    """
    Fetches details of a specific dialogue by ID, including the script and trigger points. This endpoint is used mainly by content creators for editing.
    """
    try:
        res = project.getDialogue_service.getDialogue(dialogueId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/puzzles/{puzzleId}",
    response_model=project.deletePuzzle_service.DeletePuzzleResponse,
)
async def api_delete_deletePuzzle(
    puzzleId: str,
) -> project.deletePuzzle_service.DeletePuzzleResponse | Response:
    """
    Deletes a specific puzzle. This is necessary for content management, allowing admins and content creators to remove outdated or inappropriate puzzles. It ensures clean and relevant content for players. The response will include a status of the deletion.
    """
    try:
        res = project.deletePuzzle_service.deletePuzzle(puzzleId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/dialogues/{dialogueId}/trigger",
    response_model=project.triggerDialogueEvent_service.DialogueTriggerResponse,
)
async def api_get_triggerDialogueEvent(
    dialogueId: str,
) -> project.triggerDialogueEvent_service.DialogueTriggerResponse | Response:
    """
    Trigger a specific dialogue event. This is used during gameplay to initiate dialogues based on player actions and game progress. It communicates with the Puzzle and Quest Modules to update the narrative flow.
    """
    try:
        res = project.triggerDialogueEvent_service.triggerDialogueEvent(dialogueId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/characters/{characterId}",
    response_model=project.updateCharacter_service.CharacterUpdateResponse,
)
async def api_put_updateCharacter(
    characterId: str,
    appearance: str,
    equippedItems: List[project.updateCharacter_service.Item],
) -> project.updateCharacter_service.CharacterUpdateResponse | Response:
    """
    Updates a character's attributes and settings. Only specific fields like appearance and equipped items can be updated by players. Admins and content creators have broader access.
    """
    try:
        res = project.updateCharacter_service.updateCharacter(
            characterId, appearance, equippedItems
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/puzzles/{puzzleId}",
    response_model=project.updatePuzzle_service.UpdatePuzzleResponse,
)
async def api_put_updatePuzzle(
    puzzleId: str, solution: str, hints: List[str], complexity: int
) -> project.updatePuzzle_service.UpdatePuzzleResponse | Response:
    """
    Updates a specific puzzle. Admins and content creators can modify puzzle data using this endpoint, such as changing the solution, hints, or complexity. The request should provide modified fields, and the response will confirm the updated status.
    """
    try:
        res = project.updatePuzzle_service.updatePuzzle(
            puzzleId, solution, hints, complexity
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/quests", response_model=project.createQuest_service.QuestCreationResponse)
async def api_post_createQuest(
    name: str, description: str, required_items: List[str], narrative: str
) -> project.createQuest_service.QuestCreationResponse | Response:
    """
    Creates a new quest. This route accepts quest details in the request body, including name, description, and required items. It interacts with the Inventory Module to verify item requirements and with the Narrative and Dialogue Module for initializing narrative elements. Expect a quest object with ID as response if successful.
    """
    try:
        res = project.createQuest_service.createQuest(
            name, description, required_items, narrative
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/multiplayer/session/{sessionId}",
    response_model=project.updateSession_service.UpdateMultiplayerSessionResponse,
)
async def api_put_updateSession(
    sessionId: str, players: List[str], gameState: str, isActive: bool
) -> project.updateSession_service.UpdateMultiplayerSessionResponse | Response:
    """
    Updates an existing multiplayer session. This may include adding/removing players, or updating the game state. It ensures reliability and consistency across client updates.
    """
    try:
        res = project.updateSession_service.updateSession(
            sessionId, players, gameState, isActive
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/quests/{questId}", response_model=project.updateQuest_service.QuestUpdateResponse
)
async def api_put_updateQuest(
    questId: str, name: str, description: str, isActive: bool
) -> project.updateQuest_service.QuestUpdateResponse | Response:
    """
    Updates an existing quest's details like name, description, and item requirements. This route is also responsible for activating or deactivating quests. Accessible only to admins and content creators to ensure controlled changes to gameplay elements.
    """
    try:
        res = project.updateQuest_service.updateQuest(
            questId, name, description, isActive
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/multiplayer/session/{sessionId}",
    response_model=project.deleteSession_service.DeleteSessionResponse,
)
async def api_delete_deleteSession(
    sessionId: str,
) -> project.deleteSession_service.DeleteSessionResponse | Response:
    """
    Deletes a specified multiplayer session. This is typically used when the game ends or all players have left the session.
    """
    try:
        res = project.deleteSession_service.deleteSession(sessionId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.patch(
    "/puzzles/{puzzleId}/complete",
    response_model=project.markPuzzleCompleted_service.PuzzleCompleteOutput,
)
async def api_patch_markPuzzleCompleted(
    puzzleId: str,
) -> project.markPuzzleCompleted_service.PuzzleCompleteOutput | Response:
    """
    Marks a puzzle as completed for a player. This endpoint updates the player's progress and possibly triggers advancements in the game's narrative or quest modules. It’s accessed when players solve a puzzle successfully. The response includes the player's updated progress.
    """
    try:
        res = project.markPuzzleCompleted_service.markPuzzleCompleted(puzzleId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/inventory/craft", response_model=project.craftItem_service.CraftingResponse)
async def api_post_craftItem(
    item_ids: List[str],
) -> project.craftItem_service.CraftingResponse | Response:
    """
    Combines specific items in the inventory to craft a new item. This requires passing an array of item IDs which will be used for crafting. Upon success, the new item is added while the old items are consumed or modified.
    """
    try:
        res = project.craftItem_service.craftItem(item_ids)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
