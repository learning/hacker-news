import sublime
import sublime_plugin

from .api import API

TITLE = 'Hacker News'

api = API()

class HackerNewsCommand(sublime_plugin.WindowCommand):
    def run(self):
        news_view = None
        window = sublime.active_window()
        for view in window.views():
            if view.settings().get("hacker_news") == 'hn':
                news_view = view

        if news_view:
            window.focus_view(news_view)
        else:
            news_view = self.create_view()

        news_view.run_command("load_top_stories")

    def create_view(self):
        view = self.window.new_file()

        # view.settings().set('color_scheme', "Packages/hacker-news/news.hidden-tmTheme")
        view.settings().set("hacker_news", 'hn')
        view.settings().set('highlight_line', True)
        view.settings().set("line_numbers", True)
        view.settings().set("font_size", 12)
        view.settings().set("spell_check", False)
        view.settings().set("scroll_past_end", False)
        view.settings().set("draw_centered", False)
        view.settings().set("line_padding_bottom", 2)
        view.settings().set("line_padding_top", 2)
        view.settings().set("caret_style", "solid")
        view.settings().set("tab_size", 4)
        view.settings().set("rulers", [])
        view.settings().set("default_encoding", "UTF-8")
        view.settings().set("show_minimap", False)
        view.settings().set("word_wrap", False)
        # view.set_syntax_file('Packages/hacker-news/news.sublime-syntax')
        view.set_scratch(True)
        view.set_name(TITLE)

        # self.disable_other_plugins(view)

        return view

class LoadTopStoriesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Remove all text
        self.view.set_read_only(False)
        selections = self.view.sel()
        full_region = sublime.Region(0, self.view.size())
        self.view.replace(edit, full_region, '')

        # Show loading
        self.view.insert(edit, 0, "Loading...")
        self.view.set_read_only(True)

        api.top_stories(lambda data: print('loaded %s' % data))
        self.view.sel().clear()
