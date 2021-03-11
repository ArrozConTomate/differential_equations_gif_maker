import numpy as np
import matplotlib.pyplot as plt

class Frame:
    
    def __init__(self, lines, lims, color, size_dots, number_of_dots_to_plot, initial_frame_of_each_line, frame_cont):
        
        self.lims = lims
        self.lines = lines
        self.color = color
        self.size_dots = size_dots
        self.number_of_dots_to_plot = number_of_dots_to_plot
        self.initial_frame_of_each_line = initial_frame_of_each_line
        self.frame_cont = frame_cont
        
    def plot_Frame(self):
        
        fig, ax = plt.subplots(figsize=(15, 15))
        
        cont_line = 0
        for line in self.lines:
            
            alphas = np.linspace(0, 1, self.number_of_dots_to_plot)
            alphas_rev = np.linspace(1, 0, self.number_of_dots_to_plot)
            
            L = np.shape(line)[1]
            In = self.initial_frame_of_each_line[cont_line]
            In = (In + self.frame_cont)%L
            
            #print(L)
            #print(self.frame_cont)
            #print(In)
            
            x_head = []
            x_tail = []
            y_head = []
            y_tail = []
            
            x = []
            y = []
            
            # Caso normal
            if In + self.number_of_dots_to_plot <= L:
                for i in range(self.number_of_dots_to_plot-1):
                    #print('0')
                    x = [line[0, In+i], line[0, In+i+1]]
                    y = [line[1, In+i], line[1, In+i+1]]
                    
                    ax.plot(x, y, color=self.color, linewidth=self.size_dots, alpha=alphas[i])
            
            # Solo pinto la cola. Queda un punto en la cabeza
            elif In + self.number_of_dots_to_plot == L+1:
                for i in range(self.number_of_dots_to_plot-2):
                    #print('1')
                    x = [line[0, (In+i)%L], line[0, (In+i+1)%L]]
                    y = [line[1, (In+i)%L], line[1, (In+i+1)%L]]
                    
                    ax.plot(x, y, color=self.color, linewidth=self.size_dots, alpha=alphas[i])
            
            # Solo pinto la cabeza. Queda un punto en la cola
            elif In == L-1:
                for i in range(1, self.number_of_dots_to_plot):
                    #print('2')
                    x = [line[0, (In+i)%L], line[0, (In+i+1)%L]]
                    y = [line[1, (In+i)%L], line[1, (In+i+1)%L]]
                    
                    ax.plot(x, y, color=self.color, linewidth=self.size_dots, alpha=alphas[i])
            
            # Parte cabeza y parte cola. Pinto las dos
            else:
                for i in range(L-In-1):
                    #print('3')
                    x_tail = [line[0, (In+i)%L], line[0, (In+i+1)%L]]
                    y_tail = [line[1, (In+i)%L], line[1, (In+i+1)%L]]
                    #print('33')
                    
                    ax.plot(x_tail, y_tail, color=self.color, linewidth=self.size_dots, alpha=alphas[i])
                    
                    
                for i in range(self.number_of_dots_to_plot-L+In-1, -1, -1):
                    #print('4')
                    x_head = [line[0, i], line[0, i+1]]
                    y_head = [line[1, i], line[1, i+1]]
                    
                    ax.plot(x_head, y_head, color=self.color, linewidth=self.size_dots, alpha=alphas[i])
                
                
            """    
            for i in range(self.number_of_dots_to_plot):
                
                if In + self.number_of_dots_to_plot <= L:
                    x = [line[0, In+i], line[0, In+i+1]]
                    y = [line[1, In+i], line[1, In+i+1]]
                    
                    ax.plot(x, y, color=self.color, linewidth=self.size_dots, alpha=alphas[i])
                
                if In + self.number_of_dots_to_plot == L+1
                
                :
                
                if i != len(line):
                    
                    x.append([line[0, i], line[0, (i+1)%len(line)]])
                    y.append([line[1, i], line[1, (i+1)%len(line)]])
                    #ax.scatter(line[0, i], line[1, i], color=self.color, s=self.size_dots, alpha=alphas[i])
                
                    ax.plot(x, y, color=self.color, linewidth=self.size_dots, alpha=alphas[i])
                else:
                    ax.scatter(line[0, i], line[1, i], color=self.color, s=self.size_dots, alpha=alphas[i])
                """
            
            cont_line += 1
            
        ax.set_xlim(self.lims[0], self.lims[1])
        ax.set_ylim(self.lims[2], self.lims[3])        
        
        fig.canvas.draw()       # draw the canvas, cache the renderer
        
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    
        return image
                
      
                
        
        
