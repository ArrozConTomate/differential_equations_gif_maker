import func_tools.renderizer as renderizer
import logging
import numpy as np
import time
import imageio

# Initialize the logger
logger = logging.getLogger(__name__)
if not len(logger.handlers):
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s ')
    
    file_handler = logging.FileHandler('GIF_maker_log.log')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)


logger.info('--------------- New GIF ---------------')

# Set the parameters:
    
# 2D vector-map fucntion
def vector_map(coords): 
    x = coords[0]
    y = coords[1]
    return([x-y+x**2*np.sin(y), -2*y+x**3]) 
    
# Parameters of the Frame object:
x_inf_lim = -110
x_sup_lim = 10
y_inf_lim = -10
y_sup_lim = 10

lims = [x_inf_lim, x_sup_lim, y_inf_lim, y_sup_lim]
color = 'b'
size_dots = 1

logger.info('Frame object parameters:')
logger.info('x_inf_lim: {}'.format(x_inf_lim))
logger.info('x_sup_lim: {}'.format(x_sup_lim))
logger.info('y_inf_lim: {}'.format(y_inf_lim))
logger.info('y_sup_lim: {}'.format(y_sup_lim))
logger.info('color: {}'.format(color))
logger.info('size_dots: {}'.format(size_dots))


    
# Parameters of the gif file
gif_name = 'Custom_ODE.gif'
number_of_dots_to_plot = 60
number_of_frames = 120
dot_step = 0.025
number_of_initial_dots = 300
fps = 60
seed = 19970905
np.random.seed(seed)

logger.info('GIF file parameters:')
logger.info('number_of_frames: {}'.format(number_of_frames))
logger.info('number_of_dots_to_plot: {}'.format(number_of_dots_to_plot))
logger.info('dot_step: {}'.format(dot_step))
logger.info('number_of_initial_dots: {}'.format(number_of_initial_dots))
logger.info('fps: {}'.format(fps))
logger.info('seed: {}'.format(seed))

               
initial_dots = []
for i in range(number_of_initial_dots):
    a = (x_sup_lim - x_inf_lim)*np.random.random()-x_sup_lim
    b = (y_sup_lim - y_inf_lim)*np.random.random()-y_sup_lim
    initial_dots.append([a, b])
    
# initial_dots = [[1,1]]
final_lines = []

time_total = 0
# Compute the dots
tic = time.time()



for initial_dot in initial_dots:
    
    line = np.zeros([2, number_of_frames])
    x_new = initial_dot[0]
    y_new = initial_dot[1]
    
    line[0, 0] = x_new
    line[1, 0] = y_new
    
    for frame_cont in range(1, number_of_frames):
        coord_new = [x_new, y_new]
        
        
        x_new = x_new + dot_step*vector_map(coord_new)[0]
        y_new = y_new + dot_step*vector_map(coord_new)[1]
        
        
        line[0, frame_cont] = x_new 
        line[1, frame_cont] = y_new 
    
    final_lines.append(line)
    
toc = time.time()
logger.info('Time to compute the initial dots images: {}'.format(toc-tic))

time_total += toc-tic        
    

# Generate the .gif file
tic = time.time()

# Shuffle the lines in each frame
initial_frame_of_each_line = np.random.randint(number_of_frames, size=number_of_initial_dots)


frames_to_plot = []   

for frame_cont in range(number_of_frames):
    
    #final_frame = final_frames[0]
    
    frame = renderizer.Frame(final_lines, lims, color, size_dots, number_of_dots_to_plot, initial_frame_of_each_line, frame_cont)

    im = frame.plot_Frame()
    frames_to_plot.append(im)
    print(round(frame_cont/number_of_frames, 2))
    
    
    

toc = time.time() 
logger.info('Time to actually plot each frame: {}'.format(toc-tic))
time_total += toc-tic

tic = time.time()
kwargs_write = {'fps':1.0, 'quantizer':'nq'}
imageio.mimsave('./gifs/' + gif_name, frames_to_plot, fps=fps)
toc = time.time()
logger.info('Time to generate the .gif file: {}'.format(toc-tic)) 
time_total += toc-tic

logger.info('Total time: {}'.format(time_total)) 
logging.shutdown()
