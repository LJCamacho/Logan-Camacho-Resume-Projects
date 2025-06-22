package edu.psu.twopass.repository;

import edu.psu.twopass.model.EmojiEntry;

import java.util.List;

public interface DataRepository {
    List<EmojiEntry> getEmojiEntries();

    void addEntry(EmojiEntry emojiEntry);

    void deleteById(String id);

    EmojiEntry getEmojiEntryById(String id);
}
