from RootApplication import RootApplication
import Actions


# Initiate root window
window = RootApplication()
window = Actions.init_window(window)
# Run the Tkinter event loop
window.root.mainloop()
