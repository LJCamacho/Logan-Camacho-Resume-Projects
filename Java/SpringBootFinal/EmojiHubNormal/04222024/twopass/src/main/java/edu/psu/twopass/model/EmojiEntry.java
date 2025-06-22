package edu.psu.twopass.model;

import java.time.LocalDate;

public record EmojiEntry(String id, String picID, String emojiName, String emojiType, LocalDate dateCreated,
                         LocalDate dateModified) {
    public EmojiEntry {
        if (picID.isBlank()) {
            throw new IllegalArgumentException("Picture of emojis is required");
        }
        if (emojiName.isBlank()) {
            throw new IllegalArgumentException("Emoji name cannot be blank");
        }

        if (emojiType.isBlank()) {
            throw new IllegalArgumentException("Password cannot be blank");
        }
    }
}
