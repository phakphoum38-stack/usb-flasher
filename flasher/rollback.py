import os
import shutil

BACKUP_DIR = "backup_version"
CURRENT_DIR = "app"


def create_backup():
    if os.path.exists(BACKUP_DIR):
        shutil.rmtree(BACKUP_DIR)

    shutil.copytree(CURRENT_DIR, BACKUP_DIR)
    print("💾 Backup created")


def rollback():
    if not os.path.exists(BACKUP_DIR):
        print("❌ No backup found")
        return False

    shutil.rmtree(CURRENT_DIR)
    shutil.copytree(BACKUP_DIR, CURRENT_DIR)

    print("🔁 Rollback completed")
    return True
