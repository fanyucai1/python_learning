文件加密 ::

    from cryptography.fernet import Fernet
    #形成密钥以及输出密钥
    key = Fernet.generate_key()
    with open("key", "wb") as key_file:
        key_file.write(key)
    f = Fernet(key)
    #读取需要加密的文件
    with open("score_template.csv", 'rb') as original_file:
        original = original_file.read()
    #加密并输出加密文件
    encrypted = f.encrypt(original)
    with open("score_template_new.csv", 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

python脚本进行加密 ::

    如对脚本test.py进行加密，建立setup.py文件，内容如下：

    from distutils.core import setup
    from Cython.Build import cythonize
    setup(ext_modules=cythonize(["test.py"])
    
    命令行运行：
    python3 setup.py build_ext --inplace

    调用test.py,可以直接在脚本里输入import test