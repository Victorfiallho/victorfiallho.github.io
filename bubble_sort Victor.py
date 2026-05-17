import tkinter as tk
import random

W, H      = 820, 420
CANVAS_H  = 300
BAR_GAP   = 3
PAD_X     = 40
PAD_Y     = 16

COR = {
    "normal":  "#5B8DEF",
    "compare": "#A0A0A0",
    "swap":    "#EF5B5B",
    "sorted":  "#5BEF9A",
    "bg":      "#111111",
    "text":    "#EEEEEE",
    "muted":   "#555555",
}


def gerar_passos(arr_original):
    arr, n, steps = arr_original[:], len(arr_original), []

    steps.append({"arr": arr[:], "j": -1, "state": "idle", "sorted_from": n})

    for i in range(n):
        for j in range(0, n - i - 1):
            steps.append({"arr": arr[:], "j": j, "state": "compare", "sorted_from": n - i})

            if arr[j] > arr[j + 1]:
                temp, arr[j], arr[j+1] = arr[j], arr[j+1], arr[j]
                steps.append({"arr": arr[:], "j": j, "state": "swap", "sorted_from": n - i})

        steps.append({"arr": arr[:], "j": -1, "state": "sorted_pass", "sorted_from": n - i - 1})

    steps.append({"arr": arr[:], "j": -1, "state": "done", "sorted_from": 0})
    return steps


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("bubble sort")
        self.root.configure(bg=COR["bg"])
        self.root.resizable(False, False)
        self._novo_array()
        self._build_ui()
        self._draw(self.steps[0])

    def _novo_array(self):
        self.arr          = random.sample(range(5, 100), 40)
        self.steps        = gerar_passos(self.arr)
        self.idx          = 0
        self.playing      = False
        self.job          = None
        self.sorted_floor = len(self.arr)

    def _build_ui(self):
        self.canvas = tk.Canvas(self.root, width=W - 40, height=CANVAS_H,
                                bg=COR["bg"], highlightthickness=0)
        self.canvas.pack(padx=20, pady=(24, 0))

        ctrl = tk.Frame(self.root, bg=COR["bg"])
        ctrl.pack(pady=20)

        self.btn_play = tk.Button(ctrl, text="play", command=self._toggle_play,
                                  bg=COR["bg"], fg=COR["text"],
                                  font=("Courier New", 11), relief="flat",
                                  activebackground=COR["bg"], activeforeground=COR["muted"],
                                  cursor="hand2", bd=0)
        self.btn_play.pack()

        self.speed = tk.IntVar(value=960)

    def _draw(self, step):
        self.canvas.delete("all")
        arr, n, j, state = step["arr"], len(step["arr"]), step["j"], step["state"]

        sf = step.get("sorted_from", n)
        if sf < self.sorted_floor:
            self.sorted_floor = sf

        bar_w = (W - 40 - 2*PAD_X - BAR_GAP*(n-1)) / n
        max_v = max(arr)

        for idx, val in enumerate(arr):
            x1 = PAD_X + idx * (bar_w + BAR_GAP)
            x2 = x1 + bar_w
            bh = (val / max_v) * (CANVAS_H - PAD_Y - 8)
            y1 = CANVAS_H - 8 - bh
            y2 = CANVAS_H - 8

            if idx >= self.sorted_floor or state == "done":
                cor = COR["sorted"]
            elif state in ("compare", "swap") and idx in (j, j + 1):
                cor = COR["compare"] if state == "compare" else COR["swap"]
            else:
                cor = COR["normal"]

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor, outline="")

    def _toggle_play(self):
        if self.steps[self.idx]["state"] == "done":
            self._novo_array()
            self._draw(self.steps[0])
            return
        self.playing = not self.playing
        self.btn_play.config(text="pause" if self.playing else "play")
        if self.playing:
            self._loop()
        elif self.job:
            self.root.after_cancel(self.job)

    def _loop(self):
        if not self.playing:
            return
        if self.idx >= len(self.steps) - 1:
            self.playing = False
            self.btn_play.config(text="play")
            return
        self.idx += 1
        self._draw(self.steps[self.idx])
        self.job = self.root.after(1000 - self.speed.get(), self._loop)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f"{W}x{H}")
    app = App(root)
    root.mainloop()