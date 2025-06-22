package edu.psu.twopass.repository.impl;

import edu.psu.twopass.model.EmojiEntry;
import edu.psu.twopass.repository.DataRepository;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;

@Repository
public class DataRepositoryImpl implements DataRepository {

    //  instance data
    private final List<EmojiEntry> emojiEntries;

    //  constructor
    public DataRepositoryImpl() {
        this.emojiEntries = new ArrayList<>();
    }

    @Override
    public List<EmojiEntry> getEmojiEntries() {
        return this.emojiEntries;
    }

    @Override
    public void addEntry(EmojiEntry emojiEntry) {
        //  add the emoji entry to the list
        this.emojiEntries.add(emojiEntry);
    }

    @Override
    public void deleteById(String id) {
        //  find the entry with the given id
        var entry = this.emojiEntries.stream()
                .filter(e -> e.id().equals(id))
                .findFirst()
                .orElse(null);

        //  if the entry was found, remove it
        if (entry != null) {
            this.emojiEntries.remove(entry);
        }
    }

    @Override
    public EmojiEntry getEmojiEntryById(String id) {
        //  find the entry with the given id
        return this.emojiEntries.stream()
                .filter(e -> e.id().equals(id))
                .findFirst()
                .orElse(null);
    }
}
