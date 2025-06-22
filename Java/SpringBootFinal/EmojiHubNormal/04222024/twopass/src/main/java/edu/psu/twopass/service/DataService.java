package edu.psu.twopass.service;

import edu.psu.twopass.model.EmojiEntry;

import java.util.List;

public interface DataService {
    List<EmojiEntry> getEmojiEntries();

    List<EmojiEntry> getFilteredEmojiEntries(String search);

    void addEmojiEntry(EmojiEntry newEntry);

    void deleteById(String id);

    EmojiEntry getEmojiEntryById(String id);
}
