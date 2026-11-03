import qiskit as qk
import qiskit_aer as qe
import check as c
from qiskit_aer.noise import NoiseModel , depolarizing_error
from collections import Counter
statement=input("Security ")
noise_setup= NoiseModel()
eror=depolarizing_error(0.01,1)
eror2=depolarizing_error(0.011,3)
noise_setup.add_all_qubit_quantum_error(eror,['h'])
noise_setup.add_all_qubit_quantum_error(eror2,['cswap'])
setup=qe.AerSimulator(noise_model=noise_setup)
def a(b,d):
      totl=0
      for i in range (min(len(b),len(d))):
                  qbit=qk.QuantumCircuit(3,1)
                  qbit.ry(b[i],1)
                  qbit.ry(d[i],2)
                  qbit.h(0)
                  qbit.cswap(0,1,2)
                  qbit.h(0)
                  mesurement=qbit.measure(0,0)
                  simulation=setup.run(qbit,shots=5000)
                  ctsq=simulation.result().get_counts()
                  if Counter(ctsq)['1'] and Counter(ctsq)['1'] > 2*(5000/100) :
                      totl+=1
                      
                  else:
                      pass
                  print(ctsq)
      return(totl)
if statement == "S":
    if len(c.a0) != len(c.a1):
        diff = abs(len(c.a0) - len(c.a1))
        print(f"Tampered file detected: Size mismatch ({diff} byte(s) difference).")
    else:
        totl = a(c.a0, c.a1)
        if totl > 0:
            print(f"{totl} tampered byte(s) located in files.")
        else:
            print("Files are not tampered.")
else:
    totl = a(c.a0, c.a1)
    diff = abs(len(c.a0) - len(c.a1))
    if diff > 0:
        print(f"Adaptive scan completed across common bytes ({diff} byte(s) length difference).")
    else:
        print("Here is the check report:")
    
    if totl > 0:
        print(f"{totl} tampered byte(s) located in files.")
    else:
        if diff > 0:
            print("Common bytes are not tampered (only length differs).")
        else:
            print("Files are not tampered.")
        