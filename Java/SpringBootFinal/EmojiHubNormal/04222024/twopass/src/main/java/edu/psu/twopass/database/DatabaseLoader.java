package edu.psu.twopass.database;

import edu.psu.twopass.model.EmojiEntry;
import edu.psu.twopass.repository.DataRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationListener;
import org.springframework.context.event.ContextRefreshedEvent;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.UUID;

@Component
public class DatabaseLoader implements ApplicationListener<ContextRefreshedEvent> {

    private final DataRepository dataRepository;

    @Autowired
    public DatabaseLoader(DataRepository dataRepository) {
        this.dataRepository = dataRepository;
    }


    //
    //  this code will run at startup of the application

    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {

        System.out.println("*** DATABASE LOADER STARTING ***");

//        var entry1 = new PasswordEntry(1, "markzuck", "s3cretp@assw0rd", "Facebook", null, LocalDate.of(2021, 3, 1));
//        var entry2 = new PasswordEntry(2, "gamer@gmail.com", "P@$$w0rd!", "Xbox", null, LocalDate.of(2024, 1, 15));

        var entry1 = new EmojiEntry(UUID.randomUUID().toString(), "zap","No think",  "Altered", null, LocalDate.of(2021, 3, 1));
        var entry2 = new EmojiEntry(UUID.randomUUID().toString(), "devil","Red Freak AI",  "AI", null, LocalDate.of(2024, 1, 15));

        dataRepository.addEntry(entry1);
        dataRepository.addEntry(entry2);
    }
}
