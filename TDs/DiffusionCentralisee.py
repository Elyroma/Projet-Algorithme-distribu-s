from mpi4py import MPI
import time, random

comm = MPI.COMM_WORLD
me = comm.Get_rank()
size = comm.Get_size()

def diffuseCentralisee(sender, msg):
    print("Hi from <"+str(me)+">")
    if me == sender:
        buf = msg
        print("I'm <"+str(me)+">: send " + buf[0])
        for i in range(0, size):
            if i != sender :
                comm.send(buf, dest=i, tag=99)
    else:
        buf = comm.recv(source=sender, tag=99)
        print("I'm <"+str(me)+">: receive " + buf[0])

def diffuseAnneau(sender, msg):
    next = (me + 1) % size
    prev = (me - 1) % size
    last = (sender - 1) % size
    print("Hi from <"+str(me)+">")
    if me != sender:
        buf = comm.recv(source=prev, tag=99)
        print("I'm <"+str(me)+">: receive " + buf[0])

    if me != last: 
        buf = msg
        print("I'm <"+str(me)+">: send " + buf[0])
        comm.send(buf, dest=next, tag=99)

def diffuseDoubleAnneau(sender, msg):
    next = (me + 1) % size
    prev = (me - 1) % size
    center = (sender + (size//2)) % size
    ecart = (center - me + size) % size
    print("Hi from <"+str(me)+">"+" my prev is "+str(prev)+" my next is "+str(next))
    if me == sender:
        buf = msg
        print("I'm <"+str(me)+">: send " + buf[0] + " to " + str(next))
        comm.send(buf, dest=next, tag=99)
        print("I'm <"+str(me)+">: send " + buf[0] + " to " + str(prev))
        comm.send(buf, dest=prev, tag=99)
    elif me == center or me == (center + 1) % size: 
        if me == center:
            buf = comm.recv(source=prev, tag=99)
            print("I'm <"+str(me)+">: receive " + buf[0] + " to " + str(prev))
        else:
            buf = comm.recv(source=next, tag=99)
            print("I'm <"+str(me)+">: receive " + buf[0] + " to " + str(next))
    else:
        if ecart <= size // 2:
            buf = comm.recv(source=prev, tag=99)
            print("I'm <"+str(me)+">: receive " + buf[0] + " to " + str(prev))
            print("I'm <"+str(me)+">: send " + buf[0] + " to " + str(next))
            comm.send(buf, dest=next, tag=99)
        else:
            buf = comm.recv(source=next, tag=99)
            print("I'm <"+str(me)+">: receive " + buf[0] + " to " + str(next))
            print("I'm <"+str(me)+">: send " + buf[0] + " to " + str(prev))
            comm.send(buf, dest=prev, tag=99)

def diffusionHyperCube(sender, msg):
    print("oui")

def barriere():
    if me == 0:
        for i in range(1, size):
            buf = comm.recv(source=i, tag=99)
            print("I'm <"+str(me)+">: receive " + buf[0] + " to " + str(i))
        print("On a tout le monde !")
        for i in range(1, size):
            print("I'm <"+str(me)+">: send end to " + str(i))
            comm.send(["end"], dest=i, tag=99)
    else:
        print("I'm <"+str(me)+">: send ok to 0")
        comm.send(["ok"], dest=0, tag=99)

def barriereMain():
    if me != 0:
        time.sleep(random.randint(0, 10))
    barriere()


msg = ["coucou :)"]
barriereMain()