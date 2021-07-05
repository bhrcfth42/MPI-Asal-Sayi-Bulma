from mpi4py import MPI #Mpi kütüphanesini ekliyoruz

#Bir sayının asal olup olmadığının kontrolünü sağlamak için fonksiyon oluşturularak true yada false şeklinde dönüş yapması sağlanıyor 
def Asal(sayi):#fonksiyon oluşturuluyor
    for i in range(2,int(sayi)):#2 den başlayıp sayıya kadar ilerlemesi için döngü oluşturuyor
      if(int(sayi)%i==0): #Eğer sayi%i kalannın olup olmadığına bakılıyor eğer kalansız bölünüyorsa içine gir demek istiyor 
          return False #Bu sayının asal olmadığını belirlemek için False değeri döndürüyor
    return True #Eğer diğer return içerisine girmezse en dışta otomatik şekilde True değerini döndürmesi sağlanıyor.

comm=MPI.COMM_WORLD
size=comm.Get_size() #Kaç process çağırdığımıza bakıyoruz size eşitliyoruz.
rank=comm.Get_rank() #Çalışan işlemcinin rankını yani hangisi olduğunu tutuyoruz

if rank==0: #çalışan işlemcinin rankı 0 yani bizim Master işlemcimiz ise aşağıdakileri yap diyoruz
    dizi=[x for x in range(1000,10000)] #Dizimizin içindeki değerleri oluşturyoruz
    uzunluk=int(len(dizi)/size); #Diziyi işlemcilere parçalı şekilde göndermek için bir işlemciye gönderilmesi gereken uzunluk hesaplanıyor.
    if size>1: #eğer toplam işlemci sayımız yani komut içinde verdiğimiz işlemci miktarı 1 den büyükse send işlemi yapacaz.
        for process_rank in range(1,size): #Döngü ile tüm işlemci ranklarını dolaşmaya başlıyoruz 1 den başlayarak size'a kadar
            comm.send(dizi[int(process_rank*uzunluk):int((process_rank+1)*uzunluk)],dest=int(process_rank)) #Burada process_rank ile uzunluğu çarparak başlangıç noktasını ve process_rank+1*uzunluk yazarakta bitiş noktasını buluyoruz. bu şekilde dizide belirlenen kısmın dest=process_rank ile gereken işlemciye gönderilmesini sağlıyoruz. 
        for x in dizi[int(rank*uzunluk):int((rank+1)*uzunluk)]: #Master Processin sadece göndermekle kalmayıp dizinin yukarda hesaplanan ilk uzunluk miktarının asal sorgusu için for döngüsüne sokuyoruz ve bu şekilde kendi dizisindeki elemanları tek tek dolaşması sağlanıyor
            asal_mi=Asal(x) #Fonksiyondan dönen bolean değeri ataması yapıyoruz
            if asal_mi: #fonksiyondan dönen değer true yani sayı asal ise aşağıdaki kodu çalıştırması için kontrolü sağlanıyor
                print(x,"\tIslemci:",rank) #Burada bulunan asal olan değer ve hangi işlemci bulduysa onun rankını yazdırıyoruz.
    else: #eğer toplam işlemci sayısı 1 tane ise yani tek işlemci çalıştırılıyorsa aşağıda belirtilen kısma girmesi sağlanarak dizi parçalanmadan asallık kontrolü yapılıyor
        for x in dizi: #Dizideki elemanlar tek tek okuması sağlanıyor
            asal_mi=Asal(x) #Fonksiyon ile asallık kontrolü sağlanıp bolean değer döndürmesi sağlanıyor
            if asal_mi: #fonksiyondan dönen değer kontrolü yapılıyor
                print(x,"\tIslemci:",rank) #eğer değer asal ise yazdırma işlemi yapması sağlanıyor
else: #Master işlemciler dışındaki yani rankları 0 olmayan diğer işlemcileri için aşağıdaki kodların çalışması istenmektedir.
    dizi=comm.recv(source=0) #Mpi recv fonksiyonu ile mesaj dinlemesi sağlanmıştır. Buradaki source=0 kısmı bizim master processten gelen mesajı almamızı sağlamıştır. ve bu gelen mesaj yeni bir dizi değerine atanmıştır.
    for x in dizi: #Gelen dizi elemanları tek tek okunması sağlanmıştır
        asal_mi=Asal(x) #Okunan elemanın asal olup olmadığı kontrolü sağlanmıştır.
        if asal_mi: #Fonksiyondan dönen değerin true yada false olması durumu kontrolü tapılmıştır.
            print(x,"\tIslemci:",rank) #eğer asal bir sayı ise ekrana önce değer sonra bu değerin asal olduğunu bulan işlemcinin rankı bastırılmıştır.