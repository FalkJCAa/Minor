from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.tabbedpanel import TabbedPanelItem


class GroupSettingsTab(TabbedPanelHeader):
    def __init__(self, update_timer, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Group Info & Settings'
        self.update_timer = update_timer

        layout = BoxLayout(orientation='vertical')

        self.group_size_input = TextInput(hint_text='Enter number of players', input_type='number')
        self.submit_group_size_button = Button(text='Submit Group Size')
        self.submit_group_size_button.bind(on_press=self.submit_group_size)
        layout.add_widget(self.group_size_input)
        layout.add_widget(self.submit_group_size_button)

        self.players_layout = GridLayout(cols=2)
        layout.add_widget(self.players_layout)

        self.content = layout

    def submit_group_size(self, instance):
        try:
            group_size = int(self.group_size_input.text)
            self.create_player_inputs(group_size)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def create_player_inputs(self, group_size):
        self.players_layout.clear_widgets()
        for i in range(1, group_size + 1):
            player_label = Label(text=f'Player {i}:')
            player_input = TextInput(hint_text='Enter player name')
            self.players_layout.add_widget(player_label)
            self.players_layout.add_widget(player_input)

        submit_players_button = Button(text='Submit Players')
        submit_players_button.bind(on_press=self.submit_players)
        self.players_layout.add_widget(submit_players_button)

    def submit_players(self, instance):
        player_names = [child.text for child in self.players_layout.children if isinstance(child, TextInput)]
        if all(player_names):
            for name in player_names:
                self.update_username(name)
            self.update_timer(0)

    def update_username(self, username):
        player_label = Label(text=f"Player: {username}")
        self.players_layout.add_widget(player_label)


class ScoreboardTab(TabbedPanelHeader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Scoreboard'
        layout = GridLayout(cols=2)
        # Add your players and scores here
        players_scores = [('Player 1', 10), ('Player 2', 20), ('Player 3', 30), ('Player 4', 40)]
        # Sort players by score in descending order
        players_scores.sort(key=lambda x: x[1], reverse=True)
        for player, score in players_scores:
            layout.add_widget(Label(text=player))
            layout.add_widget(Label(text=str(score)))
        self.content = layout
        
class SettingsTab(TabbedPanelHeader):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Settings'
        layout = BoxLayout(orientation='vertical', spacing=10)

        # Add your settings widgets here
        setting_label = Label(text='Some Setting:')
        setting_input = TextInput(hint_text='Enter setting value')
        layout.add_widget(setting_label)
        layout.add_widget(setting_input)

        save_button = Button(text='Save Settings', on_press=self.save_settings)
        layout.add_widget(save_button)

        self.content = layout

    def save_settings(self, instance):
        # Add code to save settings here
        print('Settings saved successfully!')


class TimerApp(App):
    def build(self):
        self.tab_panel = TabbedPanel(do_default_tab=False)

        home_tab = TabbedPanelItem(text='Home')
        home_tab.add_widget(self.create_home_screen())
        self.tab_panel.add_widget(home_tab)

        group_settings_tab = GroupSettingsTab(update_timer=self.update_timer, text='Group Info & Settings')
        self.tab_panel.add_widget(group_settings_tab)

        global_score_tab = TabbedPanelItem(text='Global Score')
        global_score_tab.add_widget(Label(text='Bag of carrots, please.'))
        self.tab_panel.add_widget(global_score_tab)

        # Additional tabs
        scoreboard_tab = ScoreboardTab(text='Scoreboard')
        self.tab_panel.add_widget(scoreboard_tab)

        Clock.schedule_interval(self.update_timer, 0.01)

        # Initialize timer variables
        self.milliseconds = self.seconds = self.minutes = self.hours = 0

        return self.tab_panel

    def create_home_screen(self):
        layout = BoxLayout(orientation='vertical', spacing=10)

        title_label = Label(text='S4D', font_size=40)
        layout.add_widget(title_label)

        buttons_container = BoxLayout(orientation='vertical', spacing=10)

        play_button = Button(text='PLAY', on_press=self.start_timer)
        stop_button = Button(text='STOP', on_press=self.stop_timer)
        reset_button = Button(text='RESET', on_press=self.reset_timer)

        buttons_container.add_widget(play_button)
        buttons_container.add_widget(stop_button)
        buttons_container.add_widget(reset_button)

        layout.add_widget(buttons_container)

        self.timer_label = Label(text='00:00:00', font_size=30)
        layout.add_widget(self.timer_label)

        return layout

    def start_timer(self, instance):
        self.stop_timer()  # Stop the timer if it's already running
        self.timer_event = Clock.schedule_interval(self.display_timer, 0.01)

    def stop_timer(self, instance=None):
        if hasattr(self, 'timer_event'):
            self.timer_event.cancel()

    def reset_timer(self, instance):
        self.stop_timer()
        self.milliseconds = self.seconds = self.minutes = self.hours = 0
        self.timer_label.text = '00:00:00'

    def display_timer(self, dt):
        self.milliseconds += 10
        if self.milliseconds == 1000:
            self.milliseconds = 0
            self.seconds += 1
            if self.seconds == 60:
                self.seconds = 0
                self.minutes += 1
                if self.minutes == 60:
                    self.minutes = 0
                    self.hours += 1

        time_str = f"{self.minutes:02d}:{self.seconds:02d}:{self.milliseconds // 10:02d}"
        self.timer_label.text = time_str

    def update_timer(self, dt):
        if hasattr(self, 'timer_event') and self.timer_event.is_triggered:
            self.display_timer(dt)


if __name__ == '__main__':
    TimerApp().run()
