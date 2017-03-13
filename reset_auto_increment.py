def auto_increment(db):
    db.engine.execute("ALTER TABLE epic_smart_phrases.Entry AUTO_INCREMENT = 1;")
