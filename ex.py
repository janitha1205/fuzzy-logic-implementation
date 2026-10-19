

import numpy as np

class fuzzyfication:
    """Simple triangular fuzzifier for inputs (e.g., Service Quality)."""
    def __init__(self, num_var,funtrangle,type):
        self.x=np.zeros([num_var,np.max(type)])
        self.type=type
        self.fun_slope=[]
        self.fun_intercept=[]
        self.fun_slope2=[]
        self.fun_intercept2=[]
        self.num_var=num_var
        self.results=[]
        self.funtrangle=funtrangle
        for i in range(self.num_var):
           
            for j in range(self.type[i]):
                  self.x[i,j]=self.funtrangle[i,j]
            
            if self.type[i]==4:
            
                
                dx1 = self.x[i,1] - self.x[i,0]
                dx2 = self.x[i,3] - self.x[i,2]
                self.fun_slope.append(1/dx1)
                self.fun_intercept.append(1-self.x[i,1]/dx1)
                self.fun_slope2.append(-1/dx2)
                self.fun_intercept2.append(1+self.x[i,2]/dx2)
            else:
                dx1 = self.x[i,1] - self.x[i,0]
                dx2 = self.x[i,2] - self.x[i,1]
                self.fun_slope.append(1/dx1)
                self.fun_intercept.append(1-self.x[i,1]/dx1)
                self.fun_slope2.append(-1/dx2)
                self.fun_intercept2.append(1+self.x[i,1]/dx2)
        
    def evaluate(self, y):
        
        for i in range(self.num_var):
            print(self.type[i] )
            if (self.type[i]==4):
                if y >= self.x[i,0] and y <= self.x[i,3]:
                    if y <= self.x[i,1]:
                        degrees = self.fun_slope[i] * y + self.fun_intercept[i]
                    else: 
                        if y >= self.x[i,1] and y<= self.x[i,2]:
                            degrees = 1.0
                        else:
                            degrees = self.fun_slope2[i] * y + self.fun_intercept2[i]
                        
                else:
                    degrees = 0.0
                self.results.append(degrees)
            else:
               if y >= self.x[i,0] and y <= self.x[i,2]:
                
                if y <= self.x[i,1]:
                    degrees = self.fun_slope[i] * y + self.fun_intercept[i]
                    print("pass")
                else:
                    degrees = self.fun_slope2[i] * y + self.fun_intercept2[i]
               else:
                degrees = 0.0
               self.results.append(degrees)
        print(self.results)
        return self.results



class centroid_sys:
    def __init__(self):
        
        self.medium_tip = (0, 0.5, 3.2)
        self.middle_tip = (0.5,3.5, 5.25)
        self.high_tip = (3.5, 6.5, 12.0)

    def _triangle_height(self, x, triangle,type):
       if type==3:
            a, b, c = triangle
            if x <= a or x >= c: return 0.0
            if a < x <= b: return (x - a) / (b - a)
            return (c - x) / (c - b)
       if type==4:
            a, b, c,d = triangle
            if x <= a or x >= d: return 0.0
            if a < x <= b: return (x - a) / (b - a)
            if b < x <= c: return 1.0
            if c < x <= d: return (d - x) / (d - c)
            return 0.0
    def sim(self,val):
        score=self.compute_tip(val)
        return score
        
    def compute_tip(self,val, resolution=1000):
        weighted_sum = 0.0
        total_area = 0.0
        val_1,val_2,val_3=val
        
        #
        for i in range(resolution + 1):
            x1 = 0 + i * (val_1 / resolution)*10
            x2 = 0 + i * (val_2 / resolution)*10
            x3 = 0 + i * (val_3 / resolution)*10
            w_m=3.3
            w_mid=5.0
            w_high=12.0
            
            clip_med = min(self._triangle_height(x1, self.medium_tip,len(self.medium_tip)), w_m)
            
            clip_mid = min(self._triangle_height(x2, self.middle_tip,len(self.middle_tip)), w_mid)
            
            clip_high = min(self._triangle_height(x3, self.high_tip,len(self.high_tip)), w_high)
            
       
            

            
            weighted_sum += x1 * clip_med + x2 * clip_mid + x3 * clip_high
            total_area += clip_med + clip_mid + clip_high
            
            
        return weighted_sum / total_area if total_area > 0 else 0.0





service_input =0.2
fuzz = fuzzyfication(num_var=3, funtrangle=np.array([[0, 3,4, 5], [4, 5.5, 7,0], [5, 7,8,10]]), type=[4, 3, 4]) 
fuzz_var = fuzz.evaluate(service_input)
dfuzz = centroid_sys()
val=dfuzz.sim(fuzz_var)
print(f"Fuzzified Service Input: {fuzz_var}") 
print(f"Centroid Value: {val}")
