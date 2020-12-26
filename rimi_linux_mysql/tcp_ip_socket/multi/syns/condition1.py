#wait notify释放当前线程 通知到其他线程去关键方法 with上下文
# wait一定在notify之前启动,如果notify之前就启动了,那么wait久没有收到通知
# conn一定要在最后关闭 conn.close 或者使用with 在启动的时候使用accquire