package edu.psu.twopass.controller;

import edu.psu.twopass.model.EmojiEntry;
import edu.psu.twopass.service.DataService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.time.LocalDate;
import java.util.UUID;

//@RestController
@Controller
public class IndexController {

    private final DataService dataService;

    @Autowired
    public IndexController(DataService dataService) {
//        this.dataService = new DataServiceImpl();   // developer managed instance
        this.dataService = dataService; // Spring managed instance
    }

    @GetMapping("/")
    public String index(Model model) {
        var entries = dataService.getEmojiEntries(); // query the database for entries
        model.addAttribute("entries", entries);
        return "index"; // This is the name of the template file (templates/index.html)
    }

    //    @PostMapping("/search")   // write access
    @GetMapping("/search")   // read access
    public String search(Model model, @RequestParam String query) {
        var entries = dataService.getFilteredEmojiEntries(query); // query the database for entries
        model.addAttribute("entries", entries);
        return "index"; // This is the name of the template file (templates/index.html)
    }

    @GetMapping("/about")
    public String about() {
        return "about"; // templates/about.html
    }

    @GetMapping("/contact")
    public String contact() {
        return "contact";   // templates/contact.html
    }


    /*
        Add password entry
     */
    @PostMapping("/add")
    public String add(@RequestParam String picID, @RequestParam String emojiName, @RequestParam String emojiType, Model model) {
//        dataService.addPasswordEntry(name, password);
//        return "redirect:/"; // redirect to the index page

        var newEntry = new EmojiEntry(UUID.randomUUID().toString(), picID,emojiName, emojiType, LocalDate.now(), LocalDate.now());
        dataService.addEmojiEntry(newEntry);
        model.addAttribute("entries", dataService.getEmojiEntries());
        return "index";
    }

    //
    //  edit emoji entry
    @GetMapping("/edit/{id}")
    public String viewEditPage(@PathVariable String id, Model model) {
        //  get the entry
        //  pass the entry to the edit page
        var entry = dataService.getEmojiEntryById(id);
        if (entry == null) {
            return "redirect:/fail";
        }
        model.addAttribute("entry", entry);
        return "edit";
    }

    @PostMapping("/edit")
    public String submitEditForm(@RequestParam String id, @RequestParam String picID, @RequestParam String emojiName, @RequestParam String emojiType, Model model) {
        //  get the entry
        //  update the entry
        //  redirect to the index page
        var entry = dataService.getEmojiEntryById(id);
        if (entry == null) {
            return "redirect:/fail";
        }

        /*
            delete the old record and add a new record since record types are immutable!
         */
        dataService.deleteById(id);

        entry = new EmojiEntry(id, picID, emojiName, emojiType, LocalDate.now(), LocalDate.now());
        dataService.addEmojiEntry(entry);
        model.addAttribute("entries", dataService.getEmojiEntries());
        return "redirect:/success";
    }


    //
    //  delete password entry
    @GetMapping("/delete/{id}")
    public String delete(@PathVariable String id, Model model) {

        var entry = dataService.getEmojiEntryById(id);
        if (entry == null) {
            return "redirect:/fail";
        }

        //  delete the entry
        //  redirect to the index page
        dataService.deleteById(id);
        model.addAttribute("entries", dataService.getEmojiEntries());
        return "redirect:/success";
    }

    @GetMapping("/success")
    public String success(Model model) {
        model.addAttribute("success", true);
        model.addAttribute("entries", dataService.getEmojiEntries());
        return "index";
    }

    @GetMapping("/fail")
    public String error(Model model) {
        model.addAttribute("error", true);
        model.addAttribute("entries", dataService.getEmojiEntries());
        return "index";
    }

    @GetMapping("/login")
    public String login() {
        return "login";
    }

}
