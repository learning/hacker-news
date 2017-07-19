import sublime
import sublime_plugin

from .api import API

TITLE = 'Hacker News'
LIMIT = 30
TEMPLATE = '''%s. %s (%s)
    %s points by %s | %s comments

'''

loaded = 0
stories = None
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
        self.view.replace(edit, sublime.Region(0, self.view.size()), '')

        # Show loading
        self.view.insert(edit, 0, "Fetching Hacker News...")
        self.view.set_read_only(True)

        api.top_stories(lambda data: load_items(self.view, edit, data[:LIMIT]))
        self.view.sel().clear()

class RenderTopStoriesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        global stories
        # Remove all text
        self.view.set_read_only(False)
        self.view.replace(edit, sublime.Region(0, self.view.size()), '')

        # Insert stories
        for i, item in enumerate(stories):
            self.view.insert(edit, self.view.size(),
                TEMPLATE % (i + 1,
                    item.get('title', 'Untitled News'),
                    item.get('url'),
                    item.get('score', 0),
                    item.get('by', 'Anonymous'),
                    item.get('descendants', 0)))


        self.view.set_read_only(True)

def load_items(view, edit, ids):
    global loaded, stories
    loaded = 0
    stories = [None] * LIMIT
    for index, id in enumerate(ids):
        (lambda i: api.item(id, lambda data: render_view(view, edit, i, data)))(index)

def render_view(view, edit, index, story):
    global loaded, stories
    stories[index] = story
    loaded += 1
    if loaded is LIMIT:
        view.run_command("render_top_stories")
