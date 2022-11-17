import gener as generators
import tests
from timeit import default_timer as timer
list_generators = [generators.PythonGen(),
                           generators.LehmerLowGen(),
                           generators.LehmerHighGen(),
                          generators.L20Gen(20),
                          generators.L89Gen(89),
                          generators.GeffeGen(),
                          generators.LibGen(),
                          generators.WolframGen(),
                          generators.BMGen(),
                         generators.BBSGen()]

tests = [tests.test_check_equlity, tests.test_check_independ, tests.test_check_homog]
alpha_list = [0.01, 0.05, 0.1]

def gen_file():
    list_generators = [generators.PythonGen(),
                           generators.LehmerLowGen(),
                           generators.LehmerHighGen(),
                          generators.L20Gen(20),
                          generators.L89Gen(89),
                          generators.GeffeGen(),
                          generators.LibGen(),
                          generators.WolframGen(),
                          generators.BMGen(),
                         generators.BBSGen()]
    file = open("resultat.txt", "w")
    
    
    for generator in list_generators:
        
        file.write(str(type(generator).__name__) + '\n')
        bytes_list = generator.gen_bytes(125000)
        
        for test in tests:
            for alpha in alpha_list:
                res = test(bytes_list, alpha)
                write_file = test.__name__ + "\t" + str(alpha) + "\t" + str(res[0]) + "\t" + str(res[1]) + "\t" + str(res[2])
                file.write(write_file + "\n")
        file.write("\n")

def main():
    
    for generator in list_generators:
        
        print("---------------------------------------------------")
        
        print(type(generator).__name__)
        
        start = timer()
        bytes_list = generator.gen_bytes(125000)
        end = timer()
        
        print(bytes_list[:16])
        
        for alpha in alpha_list:
            for test in tests:
                
                print(test.__name__, test(bytes_list, alpha)[0])
            
            print("Time:", end - start)
            
        print("---------------------------------------------------")
            
    gen_file()

main()
