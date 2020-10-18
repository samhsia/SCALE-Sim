import os, sys

def gen_config(topology, acc_num, array_dim, i_sram_size, w_sram_size, o_sram_size):
    model = topology[0:6]
    filename = ACC_DIR+"acc_"+str(acc_num)+"_"+model+".cfg"

    file_config = open(filename, 'w')
    file_config.write("[general]\n")

    run_name = "\""+"acc_"+str(acc_num)+"_"+model+"\""
    file_config.write("run_name="+run_name+"\n\n")

    file_config.write("[architecture_presets]\n")
    file_config.write("ArrayHeight:"+str(array_dim[0])+"\n")
    file_config.write("ArrayWidth:"+str(array_dim[1])+"\n")

    file_config.write("IfmapSramSz:"+str(i_sram_size)+"\n")
    file_config.write("FilterSramSz:"+str(w_sram_size)+"\n")
    file_config.write("OfmapSramSz:"+str(o_sram_size)+"\n")

    file_config.write("IfmapOffset:"+str(0)+"\n")
    file_config.write("FilterOffset:"+str(10000000)+"\n")
    file_config.write("OfmapOffset:"+str(20000000)+"\n")

    file_config.write("Dataflow:"+"ws"+"\n")

    file_config.close()

def run_config(topology, acc_num):
    model    = topology[0:6]
    topology = TOPOLOGIES_DIR+topology
    acc      = ACC_DIR+"acc_"+str(acc_num)+"_"+model+".cfg"
    
    cmd   = "python3 scale.py -arch_config="+acc+" -network="+topology

    os.system(cmd)

if __name__ == '__main__':

    TOPOLOGIES_DIR = "./topologies/recommendation/"
    ACC_DIR        = "./configs/multistage_acc/"

    if not os.path.exists(TOPOLOGIES_DIR):
        os.system("mkdir "+TOPOLOGIES_DIR)
    if not os.path.exists(ACC_DIR):
        os.system("mkdir "+ACC_DIR)

    array_dims = [[16, 16], [32, 32]]
    i_sram_sizes = [512, 1024]
    w_sram_sizes = [512, 1024]
    o_sram_sizes = [512, 1024]

    topologies = ["dlrm_0_e4_bs16.csv", "dlrm_1_e16_bs64.csv"]

    for topology in topologies:
        for acc_num in range(len(array_dims)):
            gen_config(topology, acc_num, array_dims[acc_num], i_sram_sizes[acc_num], w_sram_sizes[acc_num], o_sram_sizes[acc_num])
            run_config(topology, acc_num)