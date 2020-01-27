def predict(sample): #sample[0]: school, sample[1]: sex, sample[2]: age, sample[3]: address, sample[4]: famsize, sample[5]: Pstatus, sample[6]: Medu, sample[7]: Fedu, sample[8]: Fjob, sample[9]: reason, sample[10]: guardian, sample[11]: traveltime, sample[12]: studytime, sample[13]: failures, sample[14]: schoolsup, sample[15]: famsup, sample[16]: paid, sample[17]: activities
  if sample[1] == 'F':
    if sample[9] == 'course':
      if sample[8] == 'other':
        if sample[13] <= 2:
          if sample[6] <= 3:
            return '1'
          elif sample[6] > 3:
            if sample[7] <= 3:
              return '1'
            elif sample[7] > 3:
              return '3'
        elif sample[13] > 2:
          if sample[2] > 16:
            return '1'
          elif sample[2] <= 16:
            return '2'
      elif sample[8] == 'services':
        if sample[14] == 'no':
          if sample[15] == 'yes':
            if sample[3] == 'U':
              if sample[7] > 2:
                return '1'
              elif sample[7] <= 2:
                if sample[0] == 'GP':
                  if sample[2] > 15:
                    return '2'
                  elif sample[2] <= 15:
                    return '1'
                elif sample[0] == 'MS':
                  return '1'
            elif sample[3] == 'R':
              return '2'
          elif sample[15] == 'no':
            if sample[6] <= 2:
              return '1'
            elif sample[6] > 2:
              return '3'
        elif sample[14] == 'yes':
          if sample[2] <= 15:
            return '2'
          elif sample[2] > 15:
            return '5'
      elif sample[8] == 'at_home':
        if sample[15] == 'yes':
          return '1'
        elif sample[15] == 'no':
          if sample[6] <= 1:
            return '3'
          elif sample[6] > 1:
            return '2'
      elif sample[8] == 'teacher':
        if sample[3] == 'U':
          return '1'
        elif sample[3] == 'R':
          return '2'
      elif sample[8] == 'health':
        return '1'
    elif sample[9] == 'reputation':
      if sample[13] <= 1:
        if sample[17] == 'yes':
          if sample[12] <= 2:
            if sample[2] > 16:
              if sample[14] == 'no':
                if sample[6] <= 3:
                  if sample[8] == 'other':
                    if sample[15] == 'yes':
                      return '2'
                    elif sample[15] == 'no':
                      return '1'
                  elif sample[8] == 'at_home':
                    return '1'
                  elif sample[8] == 'services':
                    return '2'
                elif sample[6] > 3:
                  return '2'
              elif sample[14] == 'yes':
                return '1'
            elif sample[2] <= 16:
              if sample[10] == 'mother':
                return '1'
              elif sample[10] == 'father':
                if sample[6] <= 1:
                  return '1'
                elif sample[6] > 1:
                  return '2'
          elif sample[12] > 2:
            return '1'
        elif sample[17] == 'no':
          if sample[10] == 'mother':
            return '1'
          elif sample[10] == 'father':
            if sample[3] == 'U':
              return '1'
            elif sample[3] == 'R':
              return '2'
          elif sample[10] == 'other':
            return '1'
      elif sample[13] > 1:
        return '2'
    elif sample[9] == 'home':
      if sample[8] == 'other':
        if sample[7] <= 2:
          if sample[6] <= 2:
            if sample[10] == 'mother':
              return '1'
            elif sample[10] == 'father':
              return '2'
            elif sample[10] == 'other':
              return '1'
          elif sample[6] > 2:
            return '2'
        elif sample[7] > 2:
          return '1'
      elif sample[8] == 'services':
        if sample[14] == 'no':
          if sample[13] <= 0:
            return '1'
          elif sample[13] > 0:
            if sample[6] <= 2:
              if sample[4] == 'GT3':
                return '1'
              elif sample[4] == 'LE3':
                return '2'
            elif sample[6] > 2:
              if sample[0] == 'GP':
                return '3'
              elif sample[0] == 'MS':
                return '1'
        elif sample[14] == 'yes':
          return '2'
      elif sample[8] == 'at_home':
        if sample[4] == 'GT3':
          return '1'
        elif sample[4] == 'LE3':
          return '2'
      elif sample[8] == 'health':
        if sample[2] > 16:
          return '1'
        elif sample[2] <= 16:
          return '2'
      elif sample[8] == 'teacher':
        if sample[5] == 'T':
          return '2'
        elif sample[5] == 'A':
          return '1'
    elif sample[9] == 'other':
      if sample[8] == 'other':
        if sample[5] == 'T':
          return '1'
        elif sample[5] == 'A':
          if sample[2] <= 15:
            return '4'
          elif sample[2] > 15:
            return '1'
      elif sample[8] == 'services':
        if sample[0] == 'MS':
          return '1'
        elif sample[0] == 'GP':
          return '2'
      elif sample[8] == 'teacher':
        if sample[0] == 'MS':
          return '4'
        elif sample[0] == 'GP':
          return '1'
      elif sample[8] == 'health':
        return '1'
      elif sample[8] == 'at_home':
        return '1'
  elif sample[1] == 'M':
    if sample[16] == 'no':
      if sample[8] == 'other':
        if sample[0] == 'GP':
          if sample[4] == 'GT3':
            if sample[11] <= 3:
              if sample[17] == 'yes':
                return '1'
              elif sample[17] == 'no':
                if sample[9] == 'course':
                  if sample[2] <= 16:
                    if sample[10] == 'mother':
                      return '1'
                    elif sample[10] == 'father':
                      return '2'
                  elif sample[2] > 16:
                    if sample[10] == 'mother':
                      return '2'
                    elif sample[10] == 'father':
                      return '1'
                elif sample[9] == 'home':
                  return '1'
                elif sample[9] == 'reputation':
                  return '1'
            elif sample[11] > 3:
              return '5'
          elif sample[4] == 'LE3':
            if sample[6] <= 2:
              if sample[11] <= 1:
                if sample[2] <= 17:
                  if sample[12] <= 1:
                    return '3'
                  elif sample[12] > 1:
                    return '1'
                elif sample[2] > 17:
                  return '2'
              elif sample[11] > 1:
                return '2'
            elif sample[6] > 2:
              if sample[10] == 'mother':
                return '1'
              elif sample[10] == 'other':
                return '2'
        elif sample[0] == 'MS':
          if sample[9] == 'course':
            if sample[15] == 'no':
              return '3'
            elif sample[15] == 'yes':
              return '5'
          elif sample[9] == 'other':
            if sample[4] == 'GT3':
              return '1'
            elif sample[4] == 'LE3':
              return '2'
          elif sample[9] == 'home':
            return '3'
      elif sample[8] == 'services':
        if sample[9] == 'course':
          if sample[13] <= 0:
            if sample[0] == 'GP':
              return '1'
            elif sample[0] == 'MS':
              return '3'
          elif sample[13] > 0:
            if sample[6] > 1:
              if sample[2] > 16:
                if sample[3] == 'U':
                  return '2'
                elif sample[3] == 'R':
                  return '1'
              elif sample[2] <= 16:
                return '1'
            elif sample[6] <= 1:
              return '2'
        elif sample[9] == 'home':
          if sample[13] <= 0:
            if sample[7] <= 3:
              return '1'
            elif sample[7] > 3:
              return '3'
          elif sample[13] > 0:
            if sample[6] <= 3:
              return '3'
            elif sample[6] > 3:
              return '2'
        elif sample[9] == 'reputation':
          if sample[12] > 1:
            if sample[5] == 'T':
              if sample[17] == 'yes':
                return '1'
              elif sample[17] == 'no':
                return '3'
            elif sample[5] == 'A':
              return '5'
          elif sample[12] <= 1:
            if sample[4] == 'GT3':
              return '3'
            elif sample[4] == 'LE3':
              return '2'
        elif sample[9] == 'other':
          if sample[0] == 'GP':
            if sample[2] <= 17:
              return '2'
            elif sample[2] > 17:
              return '5'
          elif sample[0] == 'MS':
            return '1'
      elif sample[8] == 'teacher':
        if sample[12] > 1:
          return '1'
        elif sample[12] <= 1:
          if sample[2] <= 15:
            return '1'
          elif sample[2] > 15:
            return '2'
      elif sample[8] == 'at_home':
        if sample[0] == 'GP':
          return '1'
        elif sample[0] == 'MS':
          return '3'
      elif sample[8] == 'health':
        if sample[5] == 'T':
          return '1'
        elif sample[5] == 'A':
          return '3'
    elif sample[16] == 'yes':
      if sample[9] == 'home':
        if sample[8] == 'other':
          if sample[3] == 'U':
            if sample[6] > 2:
              if sample[7] <= 3:
                if sample[11] <= 1:
                  if sample[2] > 15:
                    return '1'
                  elif sample[2] <= 15:
                    if sample[4] == 'GT3':
                      return '2'
                    elif sample[4] == 'LE3':
                      return '1'
                elif sample[11] > 1:
                  return '2'
              elif sample[7] > 3:
                if sample[2] <= 15:
                  return '1'
                elif sample[2] > 15:
                  return '4'
            elif sample[6] <= 2:
              if sample[2] > 15:
                if sample[13] <= 0:
                  return '5'
                elif sample[13] > 0:
                  return '2'
              elif sample[2] <= 15:
                return '1'
          elif sample[3] == 'R':
            if sample[0] == 'MS':
              return '4'
            elif sample[0] == 'GP':
              return '3'
        elif sample[8] == 'teacher':
          if sample[4] == 'GT3':
            if sample[0] == 'MS':
              return '1'
            elif sample[0] == 'GP':
              return '5'
          elif sample[4] == 'LE3':
            return '2'
        elif sample[8] == 'services':
          if sample[17] == 'yes':
            return '1'
          elif sample[17] == 'no':
            return '3'
        elif sample[8] == 'health':
          return '2'
        elif sample[8] == 'at_home':
          return '2'
      elif sample[9] == 'course':
        if sample[2] > 15:
          if sample[3] == 'U':
            if sample[4] == 'LE3':
              if sample[15] == 'no':
                if sample[6] > 2:
                  if sample[8] == 'other':
                    return '4'
                  elif sample[8] == 'services':
                    return '1'
                elif sample[6] <= 2:
                  return '1'
              elif sample[15] == 'yes':
                return '4'
            elif sample[4] == 'GT3':
              if sample[8] == 'other':
                if sample[0] == 'GP':
                  if sample[12] > 2:
                    return '2'
                  elif sample[12] <= 2:
                    return '1'
                elif sample[0] == 'MS':
                  return '2'
              elif sample[8] == 'services':
                return '4'
          elif sample[3] == 'R':
            return '2'
        elif sample[2] <= 15:
          return '1'
      elif sample[9] == 'reputation':
        if sample[7] <= 3:
          return '1'
        elif sample[7] > 3:
          if sample[8] == 'other':
            if sample[2] > 16:
              return '3'
            elif sample[2] <= 16:
              return '2'
          elif sample[8] == 'teacher':
            return '1'
          elif sample[8] == 'services':
            return '1'
      elif sample[9] == 'other':
        if sample[8] == 'services':
          if sample[10] == 'mother':
            if sample[15] == 'yes':
              if sample[6] <= 1:
                return '1'
              elif sample[6] > 1:
                return '5'
            elif sample[15] == 'no':
              return '2'
          elif sample[10] == 'father':
            return '2'
          elif sample[10] == 'other':
            return '4'
        elif sample[8] == 'other':
          if sample[2] > 16:
            return '3'
          elif sample[2] <= 16:
            return '2'
        elif sample[8] == 'health':
          return '1'

  print('No classification achieved. Check features of the sample')
  return False
