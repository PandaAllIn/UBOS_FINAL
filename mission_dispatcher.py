import sys
import argparse
from pathlib import Path

# Add trinity to the python path
trinity_path = Path('/srv/janus/trinity/')
sys.path.insert(0, str(trinity_path))
sys.path.insert(0, str(Path('/srv/janus/')))


from trinity.mission_queue_manager import MissionQueueManager

def main():
    """Assigns a specific queued mission to its designated resident."""
    parser = argparse.ArgumentParser(description="Assign a mission to a resident.")
    parser.add_argument("mission_id", help="The ID of the mission to assign.")
    args = parser.parse_args()

    manager = MissionQueueManager()

    print(f"Attempting to assign mission {args.mission_id}...")

    # The mission_id might be the full filename, so we strip the suffix
    mission_id_base = Path(args.mission_id).stem

    mission_file = manager._mission_file("queued", mission_id_base)
    if not mission_file:
        print(f"❌ Mission {args.mission_id} not found in queued missions.")
        return 1

    mission_data = manager.load_mission(mission_file)
    resident = mission_data.get("assigned_to")

    if not resident:
        print(f"❌ Mission {args.mission_id} has no assigned resident.")
        return 1

    assigned_mission = manager.assign_mission(resident)

    if assigned_mission:
        print(f"✅ Successfully assigned mission {assigned_mission['mission_id']} to {resident}.")
    else:
        print(f"❌ Failed to assign mission {args.mission_id} to {resident}.")


if __name__ == "__main__":
    sys.exit(main())