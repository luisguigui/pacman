import tkinter as tk
import random, json, os, math, sys, threading

# (Mantive as funções de som, save e mapa idênticas para não poluir o código)
def _beep(freq, ms):
    try:
        if sys.platform == "win32":
            import winsound; winsound.Beep(int(freq), int(ms))
    except: pass

def som(freq, ms):
    threading.Thread(target=_beep, args=(freq, ms), daemon=True).start()

SAVE = "pacman_save.json"
def salvar(nivel, score):
    d = load_save()
    d["level"] = max(nivel, d["level"]); d["highscore"] = max(score, d["highscore"])
    try:
        with open(SAVE, "w") as f: json.dump(d, f)
    except: pass

def load_save():
    try:
        if os.path.exists(SAVE):
            with open(SAVE) as f: return json.load(f)
    except: pass
    return {"level": 1, "highscore": 0}

def gerar_mapa(cols=23, rows=23):
    m = [[1]*cols for _ in range(rows)]
    for y in range(1, rows-1):
        for x in range(1, cols-1):
            if y % 2 == 1 or x % 2 == 1: m[y][x] = 0
    cantos = [(1,1),(cols-2,1),(1,rows-2),(cols-2,rows-2)]
    for cx, cy in cantos: m[cy][cx] = 3
    return m

COLS, ROWS = 23, 23
CELL = 26
W, H = COLS * CELL, ROWS * CELL
TICK_BASE, MIN_TICK = 90, 38

BG, WALL_C, WALL_G = "#000011", "#0033cc", "#002299"
PILL_C, POWER_C, PAC_C, PAC_EDGE = "#ffaaaa", "#ffffff", "#ffee00", "#ffaa00"
GHOST_C = {"blinky":"#ff2222","pinky":"#ff99ff","inky":"#22ffff","clyde":"#ffaa22"}
VUL_C, VUL_END, EYE_W, EYE_B, HUD_BG, GOLD, CYAN = "#1133ff", "#aaaaff", "#ffffff", "#0000ff", "#000022", "#ffdd00", "#00ffcc"

def cx(gx): return gx * CELL + CELL//2
def cy(gy): return gy * CELL + CELL//2
def pode(mapa, x, y): return 0 <= x < COLS and 0 <= y < ROWS and mapa[y][x] != 1
def dirs_livres(mapa, x, y): return [(dx,dy) for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)] if pode(mapa, x+dx, y+dy)]

class Ghost:
    BASES = {"blinky":(COLS-2,1),"pinky":(COLS-2,ROWS-2),"inky":(1,ROWS-2),"clyde":(COLS//2,ROWS//2)}
    def __init__(self, tipo):
        self.tipo = tipo
        self.bx, self.by = self.BASES[tipo]
        self.x, self.y = self.bx, self.by
        self.vul, self.vt, self.morto = False, 0, False
        self.dir = (0,0)
    def reset(self): self.x, self.y = self.bx, self.by; self.vul=False; self.vt=0; self.morto=False
    def set_vul(self, ms): 
        if not self.morto: self.vul=True; self.vt=ms
    def tick(self, dt):
        if self.vul:
            self.vt -= dt
            if self.vt <= 0: self.vul=False; self.vt=0
    @property
    def piscando(self): return self.vul and self.vt < 2000
    def mover(self, mapa, px, py, nivel, tick):
        if tick % 2 != 0: return 
        livres = dirs_livres(mapa, self.x, self.y)
        if not livres: return
        if self.morto:
            melhor = min(livres, key=lambda d: abs(self.x+d[0]-self.bx)+abs(self.y+d[1]-self.by))
            self.x+=melhor[0]; self.y+=melhor[1]
            if self.x==self.bx and self.y==self.by: self.morto=False
            return
        nao_reverso = [(dx,dy) for dx,dy in livres if (dx,dy)!=(-self.dir[0],-self.dir[1])]
        candidatos = nao_reverso if nao_reverso else livres
        intel = min(0.15 + nivel*0.02, 0.92)
        if self.vul: melhor = max(candidatos, key=lambda d: (self.x+d[0]-px)**2+(self.y+d[1]-py)**2)
        elif random.random() < intel:
            if self.tipo=="blinky": alvo=(px,py)
            elif self.tipo=="pinky": alvo=(min(px+3,COLS-1), min(py+3,ROWS-1))
            elif self.tipo=="inky": alvo=(px,py) if random.random()<0.5 else (self.bx,self.by)
            else: dist=abs(self.x-px)+abs(self.y-py); alvo=(px,py) if dist>6 else (self.bx,self.by)
            melhor = min(candidatos, key=lambda d: abs(self.x+d[0]-alvo[0])+abs(self.y+d[1]-alvo[1]))
        else: melhor = random.choice(candidatos)
        self.dir = melhor; self.x += melhor[0]; self.y += melhor[1]

# ─── App com Lógica de Tela Cheia ──────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PAC-MAN EVOLUTION")
        self.configure(bg=HUD_BG)
        
        # Iniciar em tela cheia (opcional)
        self.is_fullscreen = False 
        
        self.save = load_save()
        self._frame = None
        
        # Binds globais: Teclado + Alternar Tela Cheia (F11)
        self.bind_all("<KeyPress>", self._handle_keypress)
        self.bind_all("<F11>", self.toggle_fullscreen)
        self.bind_all("<Escape>", self.exit_fullscreen)
        
        self.ir_menu()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.attributes("-fullscreen", False)
        # Se estiver no jogo, o Esc também serve para pausar, 
        # então o evento continua sendo propagado.

    def _handle_keypress(self, e):
        if hasattr(self._frame, "_key"): self._frame._key(e)

    def _trocar(self, frame_cls, **kw):
        if self._frame: self._frame.destroy()
        # Centraliza o conteúdo no meio da tela se estiver em Fullscreen
        self._frame = frame_cls(self, **kw)
        self._frame.pack(expand=True)

    def ir_menu(self): self.save = load_save(); self._trocar(MenuFrame)
    def ir_selecao(self): self._trocar(SelecaoFrame)
    def ir_jogo(self, nivel): self._trocar(JogoFrame, nivel=nivel)
    def ir_gameover(self, nivel, score, venceu): self._trocar(GameOverFrame, nivel=nivel, score=score, venceu=venceu)

class MenuFrame(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=HUD_BG)
        c = tk.Canvas(self, width=W, height=200, bg=HUD_BG, highlightthickness=0); c.pack(pady=(30,0))
        for off, alpha in [(4,"#003311"),(2,"#006622"),(0,GOLD)]:
            c.create_text(W//2+off, 70+off, text="PAC-MAN", font=("Courier",52,"bold"), fill=alpha)
        c.create_text(W//2, 130, text="E V O L U T I O N", font=("Courier",16), fill=CYAN)
        for i,(t,cor) in enumerate(GHOST_C.items()): self._ghost_icon(c, W//2+(i-1.5)*70, 175, cor)
        tk.Label(self, text=f"RECORDE {app.save['highscore']:,}   FASE {app.save['level']}", font=("Courier",12), fg=CYAN, bg=HUD_BG).pack(pady=14)
        for txt, cmd, bg, fg in [("▶ JOGAR", lambda: app.ir_jogo(app.save["level"]), PAC_C, "#000"), ("☰ FASES", app.ir_selecao, "#1133aa","#fff"), ("✕ SAIR", app.quit, "#220000","#ff4444")]:
            tk.Button(self, text=txt, font=("Courier",14,"bold"), width=22, bg=bg, fg=fg, relief="flat", pady=9, command=cmd).pack(pady=6)

    def _ghost_icon(self, c, x, y, cor):
        r = 14
        c.create_oval(x-r,y-r,x+r,y+r, fill=cor, outline=""); c.create_rectangle(x-r,y,x+r,y+r, fill=cor, outline="")
        for i in range(2): 
            ex = x-7 if i==0 else x+1
            c.create_oval(ex,y-5,ex+6,y+2, fill=EYE_W, outline="")
            c.create_oval(ex+2,y-3,ex+4,y+1, fill=EYE_B, outline="")

class SelecaoFrame(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=HUD_BG)
        self.app, self.pg = app, (app.save["level"]-1)//20
        tk.Label(self, text="SELECIONAR FASE", font=("Courier",20,"bold"), fg=PAC_C, bg=HUD_BG).pack(pady=14)
        self.grid_f = tk.Frame(self, bg=HUD_BG); self.grid_f.pack(padx=20, pady=10)
        tk.Button(self, text="← MENU", bg="#111133", fg="#9999bb", relief="flat", command=app.ir_menu).pack(pady=6)
        self._render()

    def _render(self):
        for w in self.grid_f.winfo_children(): w.destroy()
        des = self.app.save["level"]
        for i in range(20):
            n = i + 1
            ok = n <= des
            tk.Button(self.grid_f, text=str(n), width=4, height=2, bg="#1133cc" if ok else "#111122", fg="#fff" if ok else "#335", state="normal" if ok else "disabled", command=lambda x=n: self.app.ir_jogo(x)).grid(row=i//4, column=i%4, padx=4, pady=4)

class JogoFrame(tk.Frame):
    def __init__(self, app, nivel):
        super().__init__(app, bg=HUD_BG)
        self.app, self.nivel, self.score, self.vidas, self.pausa, self._job, self._tick = app, nivel, 0, 3, False, None, 0
        self.mapa = gerar_mapa(); self._total = sum(c in (0,3) for row in self.mapa for c in row); self._comidos = 0
        self.px, self.py, self.dx, self.dy, self._nx, self._ny, self._ang, self._ang_d = 1, 1, 1, 0, 1, 0, 30, -1
        self.mapa[1][1] = 2
        self.ghosts = [Ghost(t) for t in ("blinky","pinky","inky","clyde")]
        self.hud = tk.Canvas(self, width=W, height=44, bg=HUD_BG, highlightthickness=0); self.hud.pack()
        self.cv = tk.Canvas(self, width=W, height=H, bg=BG, highlightthickness=2, highlightbackground="#1133aa"); self.cv.pack()
        self._pills, self._pac_ids, self._g_ids = {}, [], {}
        self._draw_walls(); self._draw_pills(); self._make_pac(); self._make_ghosts(); self._draw_hud()
        self.focus_force()
        self._loop()

    def _draw_walls(self):
        for y,row in enumerate(self.mapa):
            for x,v in enumerate(row):
                if v == 1:
                    ox,oy = x*CELL, y*CELL
                    self.cv.create_rectangle(ox,oy,ox+CELL,oy+CELL, fill=WALL_G, outline="")
                    self.cv.create_rectangle(ox+2,oy+2,ox+CELL-2,oy+CELL-2, fill=WALL_C, outline="")

    def _draw_pills(self):
        for y,row in enumerate(self.mapa):
            for x,v in enumerate(row):
                if v in (0,3):
                    px_, py_ = cx(x), cy(y)
                    if v==3:
                        self.cv.create_oval(px_-9,py_-9,px_+9,py_+9, fill="#334466", outline=POWER_C, width=1)
                        pid = self.cv.create_oval(px_-6,py_-6,px_+6,py_+6, fill=POWER_C, outline="")
                    else:
                        pid = self.cv.create_oval(px_-3,py_-3,px_+3,py_+3, fill=PILL_C, outline="")
                    self._pills[(x,y)] = pid

    def _make_pac(self):
        self._pac_ids = [self.cv.create_arc(0,0,1,1, fill=PAC_EDGE, outline="", start=30, extent=300), self.cv.create_arc(0,0,1,1, fill=PAC_C, outline="", start=30, extent=300)]
        self._update_pac()

    def _make_ghosts(self):
        for g in self.ghosts:
            self._g_ids[g.tipo] = {"body": self.cv.create_oval(0,0,1,1, fill=GHOST_C[g.tipo], outline=""), "skirt": self.cv.create_polygon(0,0, fill=GHOST_C[g.tipo], outline=""), "e1w": self.cv.create_oval(0,0,1,1, fill=EYE_W, outline=""), "e2w": self.cv.create_oval(0,0,1,1, fill=EYE_W, outline=""), "e1b": self.cv.create_oval(0,0,1,1, fill=EYE_B, outline=""), "e2b": self.cv.create_oval(0,0,1,1, fill=EYE_B, outline="")}

    def _update_pac(self):
        ox, oy, r = self.px*CELL+1, self.py*CELL+1, CELL-2
        ang = self._ang
        self.cv.coords(self._pac_ids[0], ox-2, oy-2, ox+r+2, oy+r+2)
        self.cv.itemconfig(self._pac_ids[0], start=ang+2, extent=360-ang*2-4)
        self.cv.coords(self._pac_ids[1], ox, oy, ox+r, oy+r)
        self.cv.itemconfig(self._pac_ids[1], start=ang, extent=360-ang*2)

    def _update_ghost(self, g):
        ids, ox, oy, r = self._g_ids[g.tipo], g.x*CELL, g.y*CELL, CELL-2
        cor = BG if g.morto else (VUL_END if g.piscando and (self._tick//3)%2==0 else (VUL_C if g.vul else GHOST_C[g.tipo]))
        self.cv.coords(ids["body"], ox+1, oy+1, ox+r, oy+r//2+r//3); self.cv.itemconfig(ids["body"], fill=cor)
        bx, by_ = ox+1, oy+r//2+r//3
        pts = [bx, oy+1, bx, by_, bx+r//2, by_+6, bx+r, by_, bx+r, oy+1]
        self.cv.coords(ids["skirt"], *pts); self.cv.itemconfig(ids["skirt"], fill=cor)
        if g.morto:
            for k in ("e1w","e2w","e1b","e2b"): self.cv.coords(ids[k], -10,-10,-9,-9)
        else:
            self.cv.coords(ids["e1w"], ox+4, oy+7, ox+9, oy+13); self.cv.coords(ids["e2w"], ox+12, oy+7, ox+17, oy+13)
            self.cv.coords(ids["e1b"], ox+5, oy+8, ox+7, oy+11); self.cv.coords(ids["e2b"], ox+13, oy+8, ox+15, oy+11)

    def _draw_hud(self):
        self.hud.delete("all")
        self.hud.create_text(10, 22, anchor="w", text=f"LVL {self.nivel}", font=("Courier",13,"bold"), fill=PAC_C)
        self.hud.create_text(W//2, 22, text=f"SCORE {self.score:,}", font=("Courier",13,"bold"), fill=CYAN)
        self.hud.create_text(W-10, 22, anchor="e", text="♥"*self.vidas, font=("Courier",13), fill="#f33")

    def _loop(self):
        if self.pausa: self._job = self.after(80, self._loop); return
        dt = max(TICK_BASE - self.nivel*2, MIN_TICK); self._tick += 1
        self._ang += self._ang_d * 4
        if self._ang <= 2 or self._ang >= 38: self._ang_d *= -1
        if pode(self.mapa, self.px+self._nx, self.py+self._ny): self.dx, self.dy = self._nx, self._ny
        if pode(self.mapa, self.px+self.dx, self.py+self.dy): self.px+=self.dx; self.py+=self.dy
        v = self.mapa[self.py][self.px]
        if v in (0,3):
            self.mapa[self.py][self.px] = 2; self._comidos += 1
            pid = self._pills.pop((self.px,self.py), None)
            if pid: self.cv.delete(pid)
            if v==3: self.score += 50; som(1100, 80); [g.set_vul(7000) for g in self.ghosts]
            else: self.score += 10; som(880,15)
        [g.tick(dt) for g in self.ghosts]; [g.mover(self.mapa, self.px, self.py, self.nivel, self._tick) for g in self.ghosts]
        for g in self.ghosts:
            if g.x==self.px and g.y==self.py and not g.morto:
                if g.vul: g.morto=True; self.score+=200; som(1500,100)
                else:
                    self.vidas -= 1; som(280, 450); self.px,self.py=1,1
                    if self.vidas <= 0: self._fim(False); return
        if self._comidos >= self._total: self._fim(True); return
        self._update_pac(); [self._update_ghost(g) for g in self.ghosts]; self._draw_hud()
        self._job = self.after(dt, self._loop)

    def _fim(self, venceu):
        if self._job: self.after_cancel(self._job)
        salvar(self.nivel+(1 if venceu else 0), self.score)
        self.app.ir_gameover(self.nivel, self.score, venceu)

    def _key(self, e):
        k = e.keysym.lower()
        m = {"w":(0,-1),"up":(0,-1),"s":(0,1),"down":(0,1),"a":(-1,0),"left":(-1,0),"d":(1,0),"right":(1,0)}
        if k in m: self._nx, self._ny = m[k]
        elif k=="escape": self.pausa = not self.pausa

class GameOverFrame(tk.Frame):
    def __init__(self, app, nivel, score, venceu):
        super().__init__(app, bg=HUD_BG)
        tk.Label(self, text="VITÓRIA!" if venceu else "GAME OVER", font=("Courier",30,"bold"), fg=CYAN if venceu else "#f33", bg=HUD_BG).pack(pady=20)
        tk.Label(self, text=f"SCORE: {score:,}", font=("Courier",16), fg=PAC_C, bg=HUD_BG).pack()
        tk.Button(self, text="MENU PRINCIPAL", command=app.ir_menu, font=("Courier",12,"bold"), bg="#1133cc", fg="#fff", pady=10, width=20).pack(pady=20)

if __name__ == "__main__":
    App().mainloop()