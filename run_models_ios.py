import os, sys

def gen_config_is(topology, acc_num, array_dim, i_sram_size, w_sram_size, o_sram_size):
    model = topology[0:-4]
    filename = ACC_DIR+"acc_"+str(acc_num)+"_"+model+"_is.cfg"

    file_config = open(filename, 'w')
    file_config.write("[general]\n")

    run_name = "\""+"acc_"+str(acc_num)+"_"+model+"_is\""
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

    file_config.write("Dataflow:"+"is"+"\n")

    file_config.close()

def gen_config_os(topology, acc_num, array_dim, i_sram_size, w_sram_size, o_sram_size):
    model = topology[0:-4]
    filename = ACC_DIR+"acc_"+str(acc_num)+"_"+model+"_os.cfg"

    file_config = open(filename, 'w')
    file_config.write("[general]\n")

    run_name = "\""+"acc_"+str(acc_num)+"_"+model+"_os\""
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

    file_config.write("Dataflow:"+"os"+"\n")

    file_config.close()

def run_config_is(topology, acc_num):
    model    = topology[0:-4]
    topology = TOPOLOGIES_DIR+topology
    acc      = ACC_DIR+"acc_"+str(acc_num)+"_"+model+"_is.cfg"
    
    cmd   = "python3 scale.py -arch_config="+acc+" -network="+topology

    os.system(cmd)

def run_config_os(topology, acc_num):
    model    = topology[0:-4]
    topology = TOPOLOGIES_DIR+topology
    acc      = ACC_DIR+"acc_"+str(acc_num)+"_"+model+"_os.cfg"
    
    cmd   = "python3 scale.py -arch_config="+acc+" -network="+topology

    os.system(cmd)

if __name__ == '__main__':

    TOPOLOGIES_DIR = "./topologies/recommendation/"
    ACC_DIR        = "./configs/multistage_acc/"
    OUTPUT_DIR     = "./outputs/"

    if not os.path.exists(TOPOLOGIES_DIR):
        print("*** Topologies do not exist!")

    if not os.path.exists(ACC_DIR):
        os.system("mkdir "+ACC_DIR)
    else:
        os.system("cd "+ACC_DIR+"; rm -r *")
        print("*** Deleting old accelerator configurations")

    if not os.path.exists(OUTPUT_DIR):
        os.system("mkdir "+OUTPUT_DIR)
    else:
        os.system("cd "+OUTPUT_DIR+"; rm -rf *")
        print("*** Deleting old output logs")

    array_dims = [[256, 256], [128, 128], [64, 64], [32, 32], [16, 16], [8,8], [4,4]]
    i_sram_sizes = [8192, 4096, 2048, 1024, 512, 256, 128]
    w_sram_sizes = [8192, 4096, 2048, 1024, 512, 256, 128]
    o_sram_sizes = [8192, 4096, 2048, 1024, 512, 256, 128]

    # topologies = ["dlrm_0_e4_bs16.csv", "dlrm_1_e16_bs64.csv"]
    topologies = sorted(os.listdir(TOPOLOGIES_DIR))
    print(topologies)

    experiment_num = 0

    for topology in topologies:
        for acc_num in range(len(array_dims)):
            print("********** Running Experiment {}/{} **********".format(experiment_num+1, len(topologies)*len(array_dims)))
            gen_config_is(topology, acc_num, array_dims[acc_num], i_sram_sizes[acc_num], w_sram_sizes[acc_num], o_sram_sizes[acc_num])
            gen_config_os(topology, acc_num, array_dims[acc_num], i_sram_sizes[acc_num], w_sram_sizes[acc_num], o_sram_sizes[acc_num])
            run_config_is(topology, acc_num)
            run_config_os(topology, acc_num)
            print("********** Finished Experiment {}/{} **********".format(experiment_num+1, len(topologies)*len(array_dims)))
            experiment_num+=1
