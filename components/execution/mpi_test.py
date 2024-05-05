from mpi4py import MPI
import pickle
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

print(rank)
if rank == 0:
    data = {'a': 7, 'b': 3.14}
    comm.send(data, dest=1, tag=11)
    data = comm.recv(source=1, tag=11)
    file_path='/bata/src/cleanCopy/components/execution/test1.pickle'
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

else:
    print("recieving")
    data = comm.recv(source=0, tag=11)
    file_path='/bata/src/cleanCopy/components/execution/test2.pickle'
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)
    comm.send(data, dest=0, tag=11)
    