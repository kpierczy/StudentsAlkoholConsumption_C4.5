def predict(sample): #sample[0]: school, sample[1]: sex, sample[2]: age, sample[3]: address, sample[4]: famsize, sample[5]: Pstatus, sample[6]: Medu, sample[7]: Fedu, sample[8]: Fjob, sample[9]: reason, sample[10]: guardian, sample[11]: traveltime, sample[12]: studytime, sample[13]: failures, sample[14]: schoolsup, sample[15]: famsup, sample[16]: paid, sample[17]: activities
  if sample[6] <= 3:
    if sample[8] == 'other':
      if sample[9] == 'course':
        if sample[5] == 'T':
          if sample[10] == 'mother':
            if sample[11] <= 2:
              if sample[7] <= 2:
                if sample[3] == 'U':
                  if sample[2] > 16:
                    if sample[12] > 1:
                      if sample[16] == 'no':
                        return 'other'
                      elif sample[16] == 'yes':
                        if sample[4] == 'GT3':
                          if sample[17] == 'yes':
                            return 'services'
                          elif sample[17] == 'no':
                            return 'other'
                        elif sample[4] == 'LE3':
                          return 'services'
                    elif sample[12] <= 1:
                      if sample[4] == 'LE3':
                        if sample[13] <= 1:
                          return 'health'
                        elif sample[13] > 1:
                          return 'other'
                      elif sample[4] == 'GT3':
                        return 'services'
                  elif sample[2] <= 16:
                    if sample[12] <= 2:
                      if sample[1] == 'M':
                        if sample[17] == 'yes':
                          return 'other'
                        elif sample[17] == 'no':
                          return 'services'
                      elif sample[1] == 'F':
                        return 'at_home'
                    elif sample[12] > 2:
                      return 'services'
                elif sample[3] == 'R':
                  if sample[4] == 'GT3':
                    if sample[12] <= 3:
                      return 'other'
                    elif sample[12] > 3:
                      return 'at_home'
                  elif sample[4] == 'LE3':
                    return 'at_home'
              elif sample[7] > 2:
                if sample[15] == 'yes':
                  if sample[0] == 'MS':
                    if sample[2] <= 17:
                      return 'health'
                    elif sample[2] > 17:
                      return 'at_home'
                  elif sample[0] == 'GP':
                    return 'at_home'
                elif sample[15] == 'no':
                  if sample[1] == 'F':
                    return 'services'
                  elif sample[1] == 'M':
                    return 'other'
            elif sample[11] > 2:
              if sample[7] <= 1:
                if sample[15] == 'yes':
                  return 'at_home'
                elif sample[15] == 'no':
                  return 'other'
              elif sample[7] > 1:
                if sample[0] == 'GP':
                  if sample[15] == 'no':
                    return 'at_home'
                  elif sample[15] == 'yes':
                    return 'services'
                elif sample[0] == 'MS':
                  return 'services'
          elif sample[10] == 'father':
            if sample[1] == 'M':
              return 'other'
            elif sample[1] == 'F':
              if sample[4] == 'GT3':
                return 'at_home'
              elif sample[4] == 'LE3':
                return 'other'
          elif sample[10] == 'other':
            if sample[0] == 'GP':
              if sample[2] <= 18:
                return 'other'
              elif sample[2] > 18:
                return 'at_home'
            elif sample[0] == 'MS':
              return 'other'
        elif sample[5] == 'A':
          if sample[11] <= 1:
            return 'services'
          elif sample[11] > 1:
            if sample[4] == 'LE3':
              if sample[0] == 'MS':
                return 'at_home'
              elif sample[0] == 'GP':
                return 'services'
            elif sample[4] == 'GT3':
              return 'other'
      elif sample[9] == 'home':
        if sample[12] > 1:
          if sample[3] == 'U':
            if sample[1] == 'F':
              if sample[14] == 'no':
                return 'other'
              elif sample[14] == 'yes':
                if sample[13] <= 0:
                  if sample[16] == 'no':
                    return 'other'
                  elif sample[16] == 'yes':
                    return 'services'
                elif sample[13] > 0:
                  return 'at_home'
            elif sample[1] == 'M':
              if sample[17] == 'yes':
                if sample[10] == 'mother':
                  if sample[2] > 15:
                    if sample[7] > 1:
                      return 'services'
                    elif sample[7] <= 1:
                      return 'other'
                  elif sample[2] <= 15:
                    return 'other'
                elif sample[10] == 'father':
                  if sample[2] > 16:
                    return 'other'
                  elif sample[2] <= 16:
                    return 'services'
                elif sample[10] == 'other':
                  return 'other'
              elif sample[17] == 'no':
                if sample[5] == 'T':
                  return 'other'
                elif sample[5] == 'A':
                  if sample[4] == 'GT3':
                    return 'other'
                  elif sample[4] == 'LE3':
                    return 'services'
          elif sample[3] == 'R':
            if sample[0] == 'GP':
              if sample[5] == 'T':
                return 'at_home'
              elif sample[5] == 'A':
                return 'other'
            elif sample[0] == 'MS':
              return 'other'
        elif sample[12] <= 1:
          if sample[1] == 'M':
            if sample[4] == 'GT3':
              if sample[7] <= 2:
                return 'other'
              elif sample[7] > 2:
                if sample[2] > 16:
                  return 'health'
                elif sample[2] <= 16:
                  return 'other'
            elif sample[4] == 'LE3':
              return 'teacher'
          elif sample[1] == 'F':
            if sample[11] > 1:
              return 'at_home'
            elif sample[11] <= 1:
              return 'other'
      elif sample[9] == 'reputation':
        if sample[7] <= 2:
          if sample[17] == 'yes':
            if sample[10] == 'mother':
              if sample[12] <= 2:
                if sample[1] == 'F':
                  if sample[15] == 'yes':
                    return 'at_home'
                  elif sample[15] == 'no':
                    if sample[2] > 16:
                      return 'other'
                    elif sample[2] <= 16:
                      return 'services'
                elif sample[1] == 'M':
                  if sample[2] <= 16:
                    return 'other'
                  elif sample[2] > 16:
                    return 'services'
              elif sample[12] > 2:
                if sample[1] == 'F':
                  return 'at_home'
                elif sample[1] == 'M':
                  if sample[2] > 16:
                    return 'services'
                  elif sample[2] <= 16:
                    return 'at_home'
            elif sample[10] == 'father':
              return 'services'
            elif sample[10] == 'other':
              return 'at_home'
          elif sample[17] == 'no':
            if sample[4] == 'GT3':
              return 'other'
            elif sample[4] == 'LE3':
              if sample[10] == 'mother':
                if sample[15] == 'no':
                  if sample[0] == 'GP':
                    return 'other'
                  elif sample[0] == 'MS':
                    return 'services'
                elif sample[15] == 'yes':
                  return 'services'
              elif sample[10] == 'other':
                return 'services'
              elif sample[10] == 'father':
                return 'other'
        elif sample[7] > 2:
          if sample[10] == 'mother':
            if sample[17] == 'yes':
              return 'other'
            elif sample[17] == 'no':
              return 'health'
          elif sample[10] == 'other':
            if sample[1] == 'F':
              return 'other'
            elif sample[1] == 'M':
              return 'at_home'
          elif sample[10] == 'father':
            if sample[1] == 'M':
              return 'other'
            elif sample[1] == 'F':
              return 'services'
      elif sample[9] == 'other':
        if sample[12] > 1:
          if sample[5] == 'T':
            if sample[1] == 'F':
              return 'at_home'
            elif sample[1] == 'M':
              if sample[0] == 'MS':
                return 'at_home'
              elif sample[0] == 'GP':
                return 'services'
          elif sample[5] == 'A':
            return 'other'
        elif sample[12] <= 1:
          return 'other'
    elif sample[8] == 'services':
      if sample[2] > 15:
        if sample[9] == 'course':
          if sample[13] <= 0:
            if sample[4] == 'GT3':
              if sample[3] == 'U':
                if sample[1] == 'F':
                  if sample[16] == 'no':
                    if sample[10] == 'father':
                      return 'services'
                    elif sample[10] == 'mother':
                      if sample[7] <= 1:
                        return 'at_home'
                      elif sample[7] > 1:
                        return 'services'
                  elif sample[16] == 'yes':
                    return 'at_home'
                elif sample[1] == 'M':
                  return 'at_home'
              elif sample[3] == 'R':
                if sample[0] == 'GP':
                  return 'at_home'
                elif sample[0] == 'MS':
                  return 'other'
            elif sample[4] == 'LE3':
              if sample[0] == 'GP':
                return 'services'
              elif sample[0] == 'MS':
                if sample[1] == 'F':
                  if sample[10] == 'mother':
                    return 'teacher'
                  elif sample[10] == 'father':
                    return 'at_home'
                elif sample[1] == 'M':
                  return 'services'
          elif sample[13] > 0:
            if sample[12] > 1:
              if sample[0] == 'GP':
                return 'other'
              elif sample[0] == 'MS':
                return 'services'
            elif sample[12] <= 1:
              if sample[0] == 'GP':
                return 'services'
              elif sample[0] == 'MS':
                return 'at_home'
        elif sample[9] == 'home':
          if sample[1] == 'F':
            if sample[5] == 'T':
              if sample[4] == 'GT3':
                if sample[14] == 'no':
                  if sample[10] == 'mother':
                    if sample[12] <= 2:
                      if sample[13] <= 2:
                        return 'services'
                      elif sample[13] > 2:
                        return 'at_home'
                    elif sample[12] > 2:
                      return 'at_home'
                  elif sample[10] == 'other':
                    if sample[7] <= 1:
                      return 'services'
                    elif sample[7] > 1:
                      return 'other'
                elif sample[14] == 'yes':
                  return 'other'
              elif sample[4] == 'LE3':
                return 'services'
            elif sample[5] == 'A':
              return 'other'
          elif sample[1] == 'M':
            if sample[5] == 'T':
              return 'other'
            elif sample[5] == 'A':
              return 'teacher'
        elif sample[9] == 'reputation':
          if sample[15] == 'yes':
            if sample[7] > 1:
              if sample[12] <= 2:
                return 'services'
              elif sample[12] > 2:
                if sample[3] == 'R':
                  return 'services'
                elif sample[3] == 'U':
                  return 'other'
            elif sample[7] <= 1:
              if sample[0] == 'MS':
                return 'other'
              elif sample[0] == 'GP':
                return 'at_home'
          elif sample[15] == 'no':
            if sample[7] > 1:
              return 'other'
            elif sample[7] <= 1:
              return 'services'
        elif sample[9] == 'other':
          if sample[10] == 'mother':
            if sample[3] == 'U':
              if sample[12] <= 2:
                return 'services'
              elif sample[12] > 2:
                return 'other'
            elif sample[3] == 'R':
              return 'other'
          elif sample[10] == 'father':
            return 'at_home'
          elif sample[10] == 'other':
            return 'at_home'
      elif sample[2] <= 15:
        if sample[9] == 'course':
          if sample[10] == 'father':
            if sample[16] == 'yes':
              return 'other'
            elif sample[16] == 'no':
              return 'services'
          elif sample[10] == 'mother':
            return 'at_home'
        elif sample[9] == 'home':
          if sample[1] == 'M':
            return 'services'
          elif sample[1] == 'F':
            return 'health'
        elif sample[9] == 'reputation':
          if sample[7] <= 2:
            return 'health'
          elif sample[7] > 2:
            return 'services'
    elif sample[8] == 'at_home':
      if sample[10] == 'mother':
        if sample[13] <= 0:
          if sample[0] == 'GP':
            return 'at_home'
          elif sample[0] == 'MS':
            return 'other'
        elif sample[13] > 0:
          return 'services'
      elif sample[10] == 'father':
        if sample[1] == 'F':
          if sample[2] > 16:
            return 'at_home'
          elif sample[2] <= 16:
            return 'other'
        elif sample[1] == 'M':
          return 'other'
      elif sample[10] == 'other':
        return 'services'
    elif sample[8] == 'health':
      if sample[10] == 'mother':
        if sample[2] <= 15:
          return 'services'
        elif sample[2] > 15:
          return 'at_home'
      elif sample[10] == 'father':
        if sample[2] > 16:
          if sample[1] == 'F':
            return 'health'
          elif sample[1] == 'M':
            return 'services'
        elif sample[2] <= 16:
          return 'other'
      elif sample[10] == 'other':
        return 'at_home'
    elif sample[8] == 'teacher':
      if sample[1] == 'F':
        return 'services'
      elif sample[1] == 'M':
        return 'at_home'
  elif sample[6] > 3:
    if sample[8] == 'other':
      if sample[12] <= 2:
        if sample[10] == 'mother':
          if sample[9] == 'course':
            if sample[16] == 'no':
              if sample[4] == 'GT3':
                if sample[2] <= 16:
                  if sample[1] == 'M':
                    return 'health'
                  elif sample[1] == 'F':
                    return 'services'
                elif sample[2] > 16:
                  return 'other'
              elif sample[4] == 'LE3':
                if sample[2] <= 16:
                  return 'teacher'
                elif sample[2] > 16:
                  return 'health'
            elif sample[16] == 'yes':
              if sample[14] == 'no':
                return 'teacher'
              elif sample[14] == 'yes':
                return 'other'
          elif sample[9] == 'home':
            if sample[1] == 'M':
              if sample[2] > 16:
                if sample[4] == 'GT3':
                  if sample[0] == 'MS':
                    return 'services'
                  elif sample[0] == 'GP':
                    return 'teacher'
                elif sample[4] == 'LE3':
                  return 'services'
              elif sample[2] <= 16:
                return 'teacher'
            elif sample[1] == 'F':
              return 'health'
          elif sample[9] == 'reputation':
            if sample[2] <= 16:
              if sample[7] <= 3:
                if sample[17] == 'yes':
                  return 'services'
                elif sample[17] == 'no':
                  return 'teacher'
              elif sample[7] > 3:
                return 'other'
            elif sample[2] > 16:
              if sample[7] > 3:
                return 'teacher'
              elif sample[7] <= 3:
                return 'other'
          elif sample[9] == 'other':
            if sample[2] > 15:
              if sample[3] == 'R':
                return 'services'
              elif sample[3] == 'U':
                return 'teacher'
            elif sample[2] <= 15:
              return 'health'
        elif sample[10] == 'father':
          if sample[17] == 'yes':
            return 'health'
          elif sample[17] == 'no':
            if sample[0] == 'MS':
              return 'other'
            elif sample[0] == 'GP':
              return 'services'
        elif sample[10] == 'other':
          if sample[1] == 'F':
            if sample[2] <= 18:
              return 'other'
            elif sample[2] > 18:
              return 'health'
          elif sample[1] == 'M':
            return 'teacher'
      elif sample[12] > 2:
        if sample[10] == 'mother':
          if sample[7] > 0:
            if sample[16] == 'yes':
              if sample[1] == 'F':
                if sample[3] == 'U':
                  if sample[2] <= 17:
                    if sample[11] <= 1:
                      return 'health'
                    elif sample[11] > 1:
                      return 'other'
                  elif sample[2] > 17:
                    return 'other'
                elif sample[3] == 'R':
                  return 'teacher'
              elif sample[1] == 'M':
                return 'teacher'
            elif sample[16] == 'no':
              return 'other'
          elif sample[7] <= 0:
            return 'teacher'
        elif sample[10] == 'father':
          return 'other'
        elif sample[10] == 'other':
          return 'health'
    elif sample[8] == 'services':
      if sample[9] == 'course':
        if sample[4] == 'GT3':
          if sample[12] > 2:
            return 'teacher'
          elif sample[12] <= 2:
            return 'services'
        elif sample[4] == 'LE3':
          if sample[2] > 15:
            return 'teacher'
          elif sample[2] <= 15:
            return 'health'
      elif sample[9] == 'reputation':
        if sample[2] <= 16:
          if sample[12] <= 3:
            return 'services'
          elif sample[12] > 3:
            if sample[5] == 'T':
              return 'health'
            elif sample[5] == 'A':
              return 'other'
        elif sample[2] > 16:
          if sample[1] == 'F':
            if sample[4] == 'GT3':
              return 'health'
            elif sample[4] == 'LE3':
              return 'teacher'
          elif sample[1] == 'M':
            return 'teacher'
      elif sample[9] == 'home':
        if sample[17] == 'yes':
          if sample[2] > 15:
            return 'teacher'
          elif sample[2] <= 15:
            if sample[1] == 'F':
              return 'health'
            elif sample[1] == 'M':
              return 'teacher'
        elif sample[17] == 'no':
          return 'health'
      elif sample[9] == 'other':
        if sample[2] > 15:
          if sample[14] == 'no':
            return 'teacher'
          elif sample[14] == 'yes':
            return 'services'
        elif sample[2] <= 15:
          return 'health'
    elif sample[8] == 'teacher':
      if sample[9] == 'course':
        if sample[14] == 'no':
          if sample[10] == 'mother':
            return 'teacher'
          elif sample[10] == 'father':
            if sample[2] > 15:
              return 'teacher'
            elif sample[2] <= 15:
              return 'services'
        elif sample[14] == 'yes':
          if sample[2] <= 17:
            return 'other'
          elif sample[2] > 17:
            return 'at_home'
      elif sample[9] == 'home':
        if sample[11] <= 1:
          if sample[16] == 'yes':
            return 'teacher'
          elif sample[16] == 'no':
            return 'services'
        elif sample[11] > 1:
          if sample[13] <= 0:
            return 'other'
          elif sample[13] > 0:
            return 'services'
      elif sample[9] == 'reputation':
        if sample[11] <= 1:
          return 'teacher'
        elif sample[11] > 1:
          return 'other'
      elif sample[9] == 'other':
        if sample[3] == 'R':
          if sample[0] == 'MS':
            return 'other'
          elif sample[0] == 'GP':
            return 'health'
        elif sample[3] == 'U':
          return 'services'
    elif sample[8] == 'health':
      if sample[9] == 'reputation':
        if sample[1] == 'F':
          if sample[2] > 15:
            return 'health'
          elif sample[2] <= 15:
            return 'teacher'
        elif sample[1] == 'M':
          return 'teacher'
      elif sample[9] == 'other':
        return 'health'
      elif sample[9] == 'home':
        return 'teacher'
    elif sample[8] == 'at_home':
      if sample[3] == 'U':
        if sample[16] == 'yes':
          if sample[0] == 'MS':
            return 'at_home'
          elif sample[0] == 'GP':
            return 'other'
        elif sample[16] == 'no':
          return 'services'
      elif sample[3] == 'R':
        return 'teacher'

  print('No classification achieved. Check features of the sample')
  return False
