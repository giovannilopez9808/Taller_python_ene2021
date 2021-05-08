!======================================================================
      module coor
       integer,parameter :: n=100  ! debe ser n=4*a*a*a
       real (kind=8) :: x(n),y(n)
       real (kind=8) :: vx(n),vy(n)
       real (kind=8) :: fx(n),fy(n)

      end module coor

      program MD
      use coor            ! Coordenadas de posicion.
      implicit none

      integer (kind=8) :: npasos
      integer (kind=8) :: i,k,j,iprint

      real (kind=8) :: pi,dum,random,r0,klj,r02,nr02
      real (kind=8) :: cut2,cutr2,dt
      real (kind=8) :: ec,u
      real (kind=8) :: epot
      real (kind=8) :: xx,yy,r2
      real (kind=8) :: r1,r6,pot,rr,fxx,fyy
      real (kind=8) :: ekin,en
      real (kind=8) :: vxi,vyi,vxx,vyy,vr
      real (kind=8) :: xi,yi

      character:: path*11,version*1
      path="../Results/"

      open(11,file='../Input/rho.txt',status='unknown')
      read(11,*) version
      open(2,file=path//'2_velo_'//version//'.dat',status='unknown')
      open(3,file=path//'3_coor_'//version//'.dat',status='unknown')
      open(5,file=path//'5_Cor_in_'//version//'.dat',status='unknown')
      open(8,file=path//'8_T_U_P_'//version//'.dat',status='unknown')
      r0=1.3
      klj=10
      npasos=200000
      iprint = npasos/1000
      cut2 = (2.5d0)**2
      dt = 0.01d0
      dum = 17367d0
      pi = 4d0 * datan(1d0)
      r02=r0**2
      nr02=1/r02
!<------------------Definicion de las coordenadas------------------>
      do i=1,n
        call limits(random)
        x(i)=(i-1)*0.9+random
        call limits(random)
        if (mod(i,2).eq.0) then
          u=0.5
        else
          u=0
        end if
        y(i)=u+random
        write(5,*) i,x(i),y(i)

        call random_number(vr)
        vx(i) = vr*cos(vr*2*pi)
        vy(i) = vr*sin(vr*2*pi)
      end do
      ec = 0
      u = 0
      do k = 1,npasos
!<-------------------Iniciañizacion de las fuerzas-------------->
        do i = 1,n
          fx(i) = 0
          fy(i) = 0
        end do
!<------------Inicializacion de la energia potencial--------------->
        epot=0
        do i=1,n-1
          j=i+1
          call distance(x,y,xx,yy,r2,n,i,j)
  !<---------------------Potencial FENE--------------->
          if (r2.lt.r02) then
            pot=-r02*klj*log(1-r2*nr02)/2
            u=u+pot
            epot=epot+pot
            rr=-klj*r0**2/(r0**2-r2)
            call forces(fx,fy,fxx,fyy,xx,yy,rr,i,j)
!<---------------Potencial de Lennard-Jones---------------->
            r1 = 1/r2
            r6 = r1**3
            pot=4*r6*(r6-1)
            u = u+pot
            epot=epot+pot
            rr = 48*r6*r1*(r6-0.5d0)
            call forces(fx,fy,fxx,fyy,xx,yy,rr,i,j)
          end if
        end do
!<----------------Calculo de la energía cinetica------------------->
        ekin=0
        do i=1,n
          vxi = vx(i)+dt*fx(i)
          vyi = vy(i)+dt*fy(i)
          vxx = 0.5d0*(vxi+vx(i))
          vyy = 0.5d0*(vyi+vy(i))
          en = vxx**2+vyy**2
          ekin = ekin+en
          ec = ec+en
          vx(i) = vxi
          vy(i) = vyi
          x(i) = x(i)+dt*vx(i)
          y(i) = y(i)+dt*vy(i)
        end do
        write(*,*)k,ekin/(3*n),epot/(n*n)
        if(mod(k,iprint).EQ.0) then
          write(2,*)k
          write(3,*)k
          do i=1,n
            write(2,*)SNGL(vx(i)),SNGL(vy(i))
            write(3,*)SNGL(x(i)),SNGL(y(i))
          end do
          write(8,*)k,ekin/(3*n),epot/(n*n)
        endif
      end do
      Close(2)
      Close(3)
      Close(5)
      Close(8)
      Close(11)
      end program MD

      subroutine limits(random)
      real (kind=8) :: random
      call random_number(random)
        random=random*0.2-0.1
      end subroutine

      subroutine distance(x,y,xx,yy,r2,n,i,j)
      real (kind=8) :: xx,yy,r2
      real (kind=8) :: x(n),y(n)
      integer (kind=8) :: i,j
        xi = x(i) 
        yi = y(i)
        xx = xi-x(j)
        yy = yi-y(j)
        r2 = xx**2+yy**2
      end subroutine

      subroutine forces(fx,fy,fxx,fyy,xx,yy,rr,i,j)
      real (kind=8) :: rr,fxx,fyy,xx,yy
      real (kind=8) :: fx(n),fy(n)
      integer (kind=8):: i,j
        fxx = rr*xx
        fyy = rr*yy
        fx(i) = fx(i)+fxx
        fy(i) = fy(i)+fyy
        fx(j) = fx(j)-fxx
        fy(j) = fy(j)-fyy
      end subroutine