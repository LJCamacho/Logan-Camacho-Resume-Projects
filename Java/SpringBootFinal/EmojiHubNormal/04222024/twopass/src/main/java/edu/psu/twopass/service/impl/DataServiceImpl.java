package edu.psu.twopass.service.impl;

import edu.psu.twopass.model.EmojiEntry;
import edu.psu.twopass.repository.DataRepository;
import edu.psu.twopass.service.DataService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class DataServiceImpl implements DataService {

    private final DataRepository dataRepository;

    @Autowired
    public DataServiceImpl(DataRepository dataRepository) {
//        this.dataRepository = new DataRepositoryImpl(); // developer managed instance
        this.dataRepository = dataRepository;   // Spring managed instance
    }

    @Override
    public List<EmojiEntry> getEmojiEntries() {
        return dataRepository.getEmojiEntries();
    }

    @Override
    public List<EmojiEntry> getFilteredEmojiEntries(String search) {
        var data = dataRepository.getEmojiEntries();
        return data.stream()
                .filter(entry -> entry.emojiName().contains(search) || entry.emojiType().contains(search))
                .toList();
    }

    @Override
    public void addEmojiEntry(EmojiEntry newEntry) {
        dataRepository.addEntry(newEntry);
    }

    @Override
    public void deleteById(String id) {
        dataRepository.deleteById(id);
    }

    @Override
    public EmojiEntry getEmojiEntryById(String id) {
        return dataRepository.getEmojiEntryById(id);
    }
}
