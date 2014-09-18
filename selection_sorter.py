import sublime
import sublime_plugin


class SortSelection(sublime_plugin.TextCommand):
    def run(self, edit, case_insensitive=True):
        self.edit = edit
        self.case_insensitive = case_insensitive
        self._sort_selection()

    def _sort_selection(self):
        selections = self.view.sel()

        non_duplicate_lines = []
        non_duplicate_selections = []
        for selection in selections:
            line = self.view.line(selection)
            if line in non_duplicate_lines:
                continue

            non_duplicate_selections.append(selection)
            non_duplicate_lines.append(self.view.line(selection))

        sorted_regions = self._sort_regions(non_duplicate_selections)
        sorted_lines = []
        sorted_lines_text = []
        for region in sorted_regions:
            line = self.view.line(region)
            sorted_lines.append(line)
            sorted_lines_text.append(self.view.substr(line))

        selections.clear()
        for i in reversed(range(len(non_duplicate_selections))):
            # print(self.view.substr(selection_lines[i]))
            # Replace the current lines with the sorted lines
            self.view.replace(self.edit,
                              non_duplicate_lines[i],
                              sorted_lines_text[i])

            # Update the selection
            start = non_duplicate_lines[i].begin() + (sorted_regions[i].begin() - sorted_lines[i].begin())
            end = start + sorted_regions[i].size()
            selections.add(sublime.Region(start, end))

    def _sort_regions(self, selections):
        morph = lambda s: s
        if self.case_insensitive:
            morph = lambda s: s.lower()

        # Sort the selection regions based on the text
        return sorted(selections, key=lambda r: morph(self.view.substr(r)))